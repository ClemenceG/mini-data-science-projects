import json
from json.decoder import JSONDecodeError
import argparse
from datetime import datetime
import collections

def clean_json(fn):
    loaded_posts = {}
    i = 0
    with open(fn) as f:
        for post in f:
            try:
                lines = json.loads(post)
                loaded_posts[i] = lines
                i+=1
            except JSONDecodeError:
                pass


    filtered_posts = {}
    i = 0
    for index in range(len(loaded_posts)):
        if ((list((loaded_posts[index]).keys())[0]) == "title") | ((list((loaded_posts[index]).keys())[0]) == "title_text"):
            try:
                datetime.strptime(loaded_posts[index]['createdAt'], "%Y-%m-%dT%H:%M:%S%z")
                filtered_posts[i] = loaded_posts[index]
                i+=1
            except (ValueError, TypeError):
                pass

    for value in filtered_posts.values():
        if "title_text" in value:
            value['title'] = value.pop("title_text")

    return filtered_posts

def export_json(number_as_keys, output_fn):
    od = collections.OrderedDict(sorted(number_as_keys.items()))
    outfile = open(output_fn, 'w')
    for value in od.values():
        json.dump(value, outfile)
        outfile.write('\n')
    outfile.close()


def main():
    parser = argparse.ArgumentParser(description='Input filename, output filename')
    parser.add_argument('-i', '--infile', help='input file path, each line in JSON format')
    parser.add_argument('-o', '--outfile', help='output file, in JSON format')

    args = parser.parse_args()

    input_filename = args.infile
    output_fn = args.outfile

    export_json(clean_json(input_filename), output_fn)



if __name__ == '__main__':
    main()
