import argparse
import json
import requests



def main():
    parser = argparse.ArgumentParser(description='Input filename')
    parser.add_argument('infile', help='input file path, each line in JSON format')

    args = parser.parse_args()

    input_filename = args.infile

    loaded_posts = []
    post_count = 0

    with open(input_filename) as f:
        for post in f:
            try:
                line = json.loads(post)
                loaded_posts.append(line['data']['title'])

                post_count+=1
            except JSONDecodeError:
                pass

    total_avg = sum(map(len, loaded_posts)) / len(loaded_posts)
    print(total_avg)


if __name__ == '__main__':
    main()
