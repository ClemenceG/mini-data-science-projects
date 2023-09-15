import pandas as pd
import argparse
import json
import random

def create_row_dict(data_dict):
    row = {}
    row["Name"] = data_dict["data"]["name"]
    row["title"] = data_dict["data"]["title"]
    row["coding"] = ""
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out_file', default='out.tsv', help="outout filename")
    parser.add_argument('json_file', help='input filename')
    parser.add_argument('num_post_output', nargs='?', help='number of posts to output', default=0, type=int)
    args = parser.parse_args()


    with open(args.json_file) as f:
        data = [json.loads(line) for line in f]


    data_size = len(data)
    num_posts_output = args.num_post_output

    list_rows = []
    if (num_posts_output == 0) | (num_posts_output >= data_size):
        for post in data:
            row = create_row_dict(post)
            list_rows.append(row)

    elif num_posts_output < data_size:
        sample_indexes = random.sample(range(1, data_size), num_posts_output)
        for index in sample_indexes:
            row = create_row_dict(data[index])
            list_rows.append(row)

    print(list_rows)
    posts_df = pd.DataFrame(list_rows, columns=['Name', 'title', 'coding'])
    posts_df.to_csv(path_or_buf=args.out_file, index=False, sep="\t")

if __name__ == '__main__':
    main()



