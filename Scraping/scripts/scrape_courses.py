import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import os.path as osp

'''
Import page
'''
def get_url_content(cache_dir, page_nb):
    url=str("https://www.mcgill.ca/study/2020-2021/courses/search?page="+page_nb)

    fname=hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_fname = osp.join(cache_dir, fname)

    contents = None
    if osp.exists(full_fname):
        soup = BeautifulSoup(open(full_fname, 'r'), 'html.parser')
        #contents = open(full_fname, 'r').read()
    else:
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')
        with open(full_fname, 'w') as fh:
            fh.write(text)

    return soup


'''
Extract courses list
'''
def extract_classes(soup):

    column_content = soup.findAll('h4', 'field-content')
    class_list = [x.string for x in column_content]

    return class_list


'''
Parse total string with course info into dictionary with CourseID, Course Name and # of credits
'''
def parse_course_line(course_content):
    divided_info = {}
    # to get courseID assume the first 2 words are the fac code and number
    splitID = course_content.split(" ", 2)
    divided_info['CourseID'] = str(splitID[0]+" "+splitID[1])

    # seperate between the name and the number of credits with " ("
    splitName = splitID[2].split(" (")
    divided_info['Course Name'] = splitName[0]
    divided_info['# of credits'] = (splitName[1].split(" "))[0]

    return divided_info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cache_dir', help="cache directory name")
    parser.add_argument('pagenb', help='page number')
    args = parser.parse_args()

    pagenb = args.pagenb

    soup = get_url_content(args.cache_dir, pagenb)

    classes = extract_classes(soup)

    row_list = []
    for class_info in classes:
        try:
            split_info = parse_course_line(class_info)
            row_list.append(split_info)
        except IndexError:
            pass
    classes_df = pd.DataFrame(row_list, columns=['CourseID', 'Course Name', '# of credits'])

    print(classes_df.to_csv(index=False))


if __name__ == "__main__":
    main()