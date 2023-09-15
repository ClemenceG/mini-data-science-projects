from unittest import TestCase
import pandas as pd

class Test(TestCase):


    def test_calc_mentions_twilight(self):
        from analysis import calc_mentions
        df = pd.DataFrame({'pony': ["other", "twilight", "twilight", "applejack", "twilight", 'twilight'],
                           'dialog': ['the story of Twilight\'s rainbow travel',
                                      'I want to go on an adventure with Fluttershy, Pinkie and Rainbow dash!',
                                      'come on Applejack you too',
                                      'an adventure with you twilight?',
                                      'sure! make sure Fluttershy comes along though',
                                      'we\'re off!']})
        ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
                       'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}
        mentions = calc_mentions(df, ponies_dict)
        self.assertEqual(list(mentions['twilight'].values()), [1/3, 0, 1/3, 1/3, 2/3])

    def test_foc_dictionary_creation(self):
        from analysis import calc_follow_on_comments
        df = pd.DataFrame({'pony': ["other", "twilight", "twilight", "applejack", "twilight", 'twilight'],
                           'dialog': ['the story of Twilight\'s rainbow travel',
                                      'I want to go on an adventure with Fluttershy, Pinkie and Rainbow dash!',
                                      'come on Applejack you too',
                                      'an adventure with you twilight?',
                                      'sure! make sure Fluttershy comes along though',
                                      'we\'re off!']})
        ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
                       'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}
        f_o_c = calc_follow_on_comments(df, ponies_dict)
        self.assertEqual(list(f_o_c['twilight'].keys()), ['applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy', 'other'] )

    def test_foc_sum_to_one(self):
        from analysis import calc_follow_on_comments
        df = pd.DataFrame({'pony': ["other", "twilight", "twilight", "applejack", "twilight", 'twilight'],
                           'dialog': ['the story of Twilight\'s rainbow travel',
                                      'I want to go on an adventure with Fluttershy, Pinkie and Rainbow dash!',
                                      'come on Applejack you too',
                                      'an adventure with you twilight?',
                                      'sure! make sure Fluttershy comes along though',
                                      'we\'re off!']})
        ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
                       'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}
        foc = calc_follow_on_comments(df, ponies_dict)
        self.assertEqual(sum(list(foc['applejack'].values())), 1)


    def test_foc_functioning_case(self):
        from analysis import calc_follow_on_comments
        df = pd.DataFrame({'pony': ["other", "twilight", "twilight", "applejack", "twilight", 'twilight'],
                           'dialog': ['the story of Twilight\'s rainbow travel',
                                      'I want to go on an adventure with Fluttershy, Pinkie and Rainbow dash!',
                                      'come on Applejack you too',
                                      'an adventure with you twilight?',
                                      'sure! make sure Fluttershy comes along though',
                                      'we\'re off!']})
        ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
                       'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}
        foc = calc_follow_on_comments(df, ponies_dict)
        self.assertEqual(list(foc['twilight'].values()), [1/2, 0, 0, 0, 0, 1/2])

    def test_foc_not_speaker_sum(self):
        from analysis import calc_follow_on_comments
        df = pd.DataFrame({'pony': ["other", "twilight", "twilight", "applejack", "twilight", 'twilight'],
                           'dialog': ['the story of Twilight\'s rainbow travel',
                                      'I want to go on an adventure with Fluttershy, Pinkie and Rainbow dash!',
                                      'come on Applejack you too',
                                      'an adventure with you twilight?',
                                      'sure! make sure Fluttershy comes along though',
                                      'we\'re off!']})
        ponies_dict = {'twilight': 'Twilight', 'applejack': 'Applejack', 'rarity': 'Rarity',
                       'pinkie': 'Pinkie', 'rainbow': 'Rainbow', 'fluttershy': 'Fluttershy'}
        foc = calc_follow_on_comments(df, ponies_dict)
        self.assertEqual(sum(list(foc['pinkie'].values())), 0)

    def test_remove_unicode(self):
        from analysis import replace_unicode
        df = pd.DataFrame({'A': ['fdsnkg sajld <U+904j> fds', 'fdskj<U+7549>', '<u+9327> fdsf'],
                           'B': ['fdsl U+9732>', '<U+8273>fds <U+3219>', 'nek <U+8372>']})
        self.assertEqual(replace_unicode(df).values.tolist(), [['fdsnkg sajld <U+904j> fds', 'fdsl U+9732>'], ['fdskj ',
                                                              ' fds  '], ['<u+9327> fdsf', 'nek  ']])

    def test_speed_error_count_words(self):
        '''
        finally function not used
        '''
        from analysis import count_words_from_list
        word_list = ['the', 'cat', ' hat']
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['the crazy lady', 'moved the cat out',
                                                       'into her lawn by the hat',
                                         'with the neighbors cat with a hat', 'she had a chat']})
        words_count_dict = count_words_from_list(df, 'B', word_list)
        self.assertEqual(list(words_count_dict.values()), [4, 2, 2])

    def test_tokenizing(self):
        from analysis import tokenize_column
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['the crazy-lady', 'moved the cat out',
                                                       'into her lawnby ...? the hat',
                                                       'with the neighbors, cat with a hat', 'she had a chat']})
        words = tokenize_column(df, 'B')
        self.assertEqual(words, ['the', 'crazy', 'lady', 'moved', 'the', 'cat', 'out', 'into', 'her', 'lawnby','the', 'hat',
                                                       'with', 'the', 'neighbors', 'cat', 'with', 'a', 'hat', 'she', 'had',
                                 'a', 'chat'])

    def test_not_5_words(self):
        from analysis import calc_non_dictionary_words
        df = pd.DataFrame({'pony': [1, 1, 3,  2, 1], 'dialog': ['tdshe hawd hawdcrazy-dsalady', 'shefda dsalady tewhe tewhe cat out',
                                                   'into her lawnby ...? the hadsfat hadsfat',
                                                   'witsa the neighbors, cat with a hat', 'shefda hawd a chfds']})

        eng_words = ['cat', 'out', 'into', 'her', 'the', 'neighbors', 'with', 'a', 'hat']

        most_common_word_3rd = sorted(calc_non_dictionary_words(df, {1:0, 2:0, 3:0}, eng_words)[3])
        self.assertEqual(most_common_word_3rd, sorted(['hadsfat', 'lawnby']))

    def test_with_5_non_list_words(self):
        from analysis import calc_non_dictionary_words
        df = pd.DataFrame({'pony': [1, 1, 3, 2, 1],
                            'dialog': ['tdshe hawd hawdcrazy dsalady chfds', 'hawdcrazy shefda dsalady tewhe tewhe cat out',
                                        'into her lawnby ...? the hadsfat hadsfat',
                                        'witsa the neighbors, cat with a hat', 'shefda hawd a']})

        eng_words = ['cat', 'out', 'into', 'her', 'the', 'neighbors', 'with', 'a', 'hat']

        most_common_word_1st = sorted(calc_non_dictionary_words(df, {1:0, 2:0, 3:0}, eng_words)[1])
        self.assertEqual(most_common_word_1st, sorted(['tewhe', 'hawd', 'dsalady', 'hawdcrazy', 'shefda']))


