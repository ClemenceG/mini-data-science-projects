import pandas as pd
import os.path as osp
import argparse
import itertools
import json
from nltk.tokenize import RegexpTokenizer
from collections import Counter


def calc_verbosity(df, line_cnt):
    series_occurence = df.pony.value_counts()
    verbosity = series_occurence.apply(lambda x:  x/line_cnt).to_dict()
    return verbosity


def calc_mentions(df, ponies_dict):
        mentions = {'twilight':{'total':0, 'applejack':0, 'rarity':0, 'pinkie':0, 'rainbow':0, 'fluttershy':0},
                    'applejack':{'total':0, 'twilight':0, 'rarity':0, 'pinkie':0, 'rainbow':0, 'fluttershy':0},
                    'rarity':{'total':0, 'twilight':0, 'applejack':0,  'pinkie':0, 'rainbow':0, 'fluttershy':0},
                    'pinkie':{'total':0, 'twilight':0, 'applejack':0, 'rarity':0,  'rainbow':0, 'fluttershy':0},
                    'rainbow':{'total':0, 'twilight':0, 'applejack':0, 'rarity':0, 'pinkie':0, 'fluttershy':0},
                    'fluttershy':{'total':0, 'twilight':0, 'applejack':0, 'rarity':0, 'pinkie':0, 'rainbow':0}}

        #for pony_speaking in poniesarr:
            #mentions[pony_speaking] = {} ||(Fluttershy)|(Rarity)|(Pinkie Pie)|(Rainbow Dash)
        for speaker in mentions:
            sel_df = df[df['pony'] == speaker]
            for index, row in sel_df.iterrows():
                line_repeats = -1
                for low_name_ment, cap_name_ment in ponies_dict.items():
                    if (speaker != low_name_ment) & (cap_name_ment in row['dialog']):
                        mentions[speaker][low_name_ment] += 1
                        mentions[speaker]['total'] += 1
                        line_repeats += 1
                if line_repeats > 0:
                    mentions[speaker]['total'] -= line_repeats


        for speaker, mentioned in mentions.items():
            if mentioned['total'] != 0:
                for pony in ponies_dict:
                    if pony != speaker:
                        mentioned[pony] = mentioned[pony] / mentioned['total']
            mentions[speaker].pop('total', None)
        return mentions

def calc_follow_on_comments(df, ponies_dict):
    ponies_dict['other'] = None
    follow_on_comments = dict.fromkeys(ponies_dict.keys())
    for follow in follow_on_comments:
        follow_on_comments[follow] = {k:0 for k in ponies_dict if (k != follow)}
        follow_on_comments[follow]['total_begin'] = 0

    prev_speaker = None
    for index, row in df.iterrows():
        curr_speaker = row['pony']
        if (curr_speaker != 'other') & (prev_speaker != curr_speaker):
            follow_on_comments[curr_speaker][prev_speaker] += 1
            follow_on_comments[curr_speaker]['total_begin'] += 1
        prev_speaker = curr_speaker


    for following, prev_dict in follow_on_comments.items():
        if follow_on_comments[following]['total_begin'] == 0:
            continue
        else:
            for pony in ponies_dict:
                if pony != following:
                    prev_dict[pony] = prev_dict[pony] / prev_dict['total_begin']
        follow_on_comments[following].pop('total_begin', None)
    ponies_dict.pop('other')
    return follow_on_comments


def replace_unicode(df):
    df_updated = df.replace(to_replace='<U\+[0-9]{4}>', value=' ', regex=True)
    return df_updated


def calc_non_dictionary_words(df, ponies_dict, eng_list):
    non_dictionary_words = {}

    for pony in ponies_dict:
        dialog_sentences = df[df['pony'] == pony]
        token_dialog = [word.lower() for word in tokenize_column(dialog_sentences, 'dialog')]
        non_english_words_in_dialog = set(token_dialog) & set(eng_list)
        words_to_count = [word for word in token_dialog if word not in non_english_words_in_dialog]
        most_common_words = [word for word, word_count in Counter(words_to_count).most_common(5)]
        non_dictionary_words[pony] = most_common_words

    return non_dictionary_words


def tokenize_column(df, column_name):

    tokenizer = RegexpTokenizer(r'\w+')
    #tokenizer = WordPunctTokenizer()
    words = []
    for index, row in df.iterrows():
         words.append(tokenizer.tokenize(row[column_name]))
    words = list(itertools.chain.from_iterable(words))
    return words


def count_words_from_list(df, column_name, word_list):
        word_count = {}
        # cfdist = ConditionalFreqDist((word in non_dic_words, [])
        for index, row in df.iterrows():
            for word in word_list:
                if word in row[column_name]:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
        return word_count


def __main__():
    parser = argparse.ArgumentParser(description='Read and analyse my Little Pony dialogue')
    parser.add_argument('path_src_file', help='path to dialogue')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default='out.json', help='output file, in JSON format')

    args = parser.parse_args()

    path_src_file = args.path_src_file


    df = pd.read_csv(f'{path_src_file}clean_dialog.csv')

    ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
            'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}

    df["pony"] = df["pony"].map(lambda x: "twilight" if x=='Twilight Sparkle' else "applejack" if x=='Applejack'
                                               else "rarity" if x=='Rarity' else "pinkie" if x=='Pinkie Pie'
                                                else "rainbow" if x=='Rainbow Dash' else "fluttershy" if x=='Fluttershy'
                                                else "other")

    df_only_ponies = df[df['pony'].str.match('twilight|applejack|fluttershy|rarity|pinkie|rainbow')]

    dict_final = {}
    line_count = len(df.index)

    dict_final['verbosity'] = calc_verbosity(df_only_ponies, line_count)
    dict_final['mentions'] = calc_mentions(df_only_ponies, ponies_dict)
    dict_final['follow_on_comments'] = calc_follow_on_comments(df, ponies_dict)

    df_only_ponies = replace_unicode(df_only_ponies)
    with open(osp.join(f'{path_src_file}', 'data', 'words_alpha.txt')) as f:
        non_eng_list = [line.rstrip('\n') for line in f]
    dict_final['non_dictionary_words'] = calc_non_dictionary_words(df_only_ponies, ponies_dict, non_eng_list)

    out = args.outfile if not(args.outfile is None) else 'json.out'
    json.dump(dict_final, out)
    out.write('\n')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    __main__()

