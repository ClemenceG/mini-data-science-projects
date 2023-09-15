import json
import argparse
import os.path as osp
from bs4 import BeautifulSoup
import hashlib
import requests


'''
Extract URL and return content if not in cache 
'''
def get_url_content(cache_dir, target_person):
    url=str("https://www.whosdatedwho.com/dating/"+target_person)

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
Extract the make
'''
def extract_relationships_from_candidate_links(candidates, person_url):
    relationships = []
    for link in candidates:

        href = link['href']

        if href.startswith('/dating') and href != str('/dating/'+person_url):
            relationships.append(href[8:])

    return relationships

'''
Extract list of the relationships
'''
def extract_relationships(soup, person_url):
    relationships = []

    # get current relationship
    status_h4 = soup.find('h4', 'ff-auto-status')

    # grab the next sibling
    key_div = status_h4.next_sibling

    # grab all the a elements
    candidate_links = key_div.find_all('a')

    relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))

    #if len(relationships) > 1:
   #     raise Exception('Too many relationships - should have only one')

    # get all prior relationships
    rels_h4 = soup.find('h4', 'ff-auto-relationships')
    sib = rels_h4.next_sibling

    while sib is not None and sib.name == 'p':
        candidate_links = sib.find_all('a')
        sib = sib.next_sibling

        relationships.extend(extract_relationships_from_candidate_links(candidate_links, person_url))


    return relationships



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help="configuration file")
    parser.add_argument('-o', '--output_fn', help='output filename')
    args = parser.parse_args()

    ###
    # read config file
    with open(args.config_file) as f:
        config_data = json.load(f)

    cache_dirname = config_data['cache_dir']
    target_people = config_data['target_people']

    ###
    # extract relationships for each person in list
    final_rels = {}
    for target_person in target_people:
        content = get_url_content(cache_dirname, target_person)
        final_rels[target_person] = extract_relationships(content, target_person)


    with open(args.output_fn, 'w') as f:
        json.dump(final_rels, f)
        f.write('\n')




if __name__ == "__main__":
    main()