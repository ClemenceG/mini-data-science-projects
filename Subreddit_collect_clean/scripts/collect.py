import argparse
import json
import requests

def export_posts(subreddits, num_posts_per_sub, outputfn):
    outfile = open(outputfn, "w")
    for subreddit_name in subreddits:
        data = requests.get(f'http://api.reddit.com/r/{subreddit_name}/new?limit={num_posts_per_sub}',
                        headers={"User-Agent":"windows:requests (by /u/clemmig)"})

        content = data.json()
        content = content['data']['children']
        for post in content:
            json.dump(post, outfile)
            outfile.write('\n')
    outfile.close()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outfile', help='output filepath')
    args = parser.parse_args()
    output_path = args.outfile

    sample1_subreddits = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews',
                          'videos', 'todayilearned']
    sample2_subreddits = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers',
                          'PublicFreakout', 'leagueoflegends','unpopularopinion']

    export_posts(sample1_subreddits, 100, str(output_path+'sample1.json'))
    export_posts(sample2_subreddits, 100, str(output_path+'sample2.json'))


if __name__ == '__main__':
    main()
