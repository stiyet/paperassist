# -*- coding: utf-8 -*-
import json
import argparse
import os
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('-f', '--file_input', help="result of spider")
    parser.add_argument('-a', '--author_list',
                        help="the author list (split by ',') you are interested in, eg: -a 'G Lample','A Ritter','R Leaman'")
    args = parser.parse_args()
    file_input = args.file_input
    author_list = []

    if args.author_list is not None:
        author_list = args.author_list.split(',')

    if file_input is None or not os.path.exists(file_input):
        print('ERROR!')
        print('CHECK THE ARGUMENTS & MAKE SURE THE INTPUT FILE EXISTS!')
        print("USE '-h' TO SEE THE USAGE.\n")
        sys.exit(0)

    if not os.path.exists('result'):
        os.mkdir('result')

    # load
    papers = json.load(open(file_input, 'r', encoding='utf-8'))

    # filter
    survey_papers = []  # survey, overview, summary, review, outline
    author_papers = []
    

    for item in papers:
        item['cited'] = int(item['cited'])
        if '年' in item['date']:
            item['date'] = int(item['date'][:-1])
        title = item['title']
        authors = item['authors']
        if 'survey' in title or 'overview' in title or 'summary' in title or 'review' in title or 'outline' in title:
            survey_papers.append(item)
        if author_list != []:
            for u in author_list:
                if u in authors:
                    author_papers.append(item)
                    break
    high_cited_papers = sorted(papers, key=lambda x: x['cited'], reverse=True)
    updated_papers = sorted(papers, key=lambda x: x['date'], reverse=True) # date sorted
    # save
    with open('./result/suvery.txt', 'w') as f:
        for t in survey_papers:
            f.write(json.dumps(t))
            f.write('\n')
    with open('./result/author.txt', 'w') as f:
        for t in author_papers:
            f.write(json.dumps(t))
            f.write('\n')
    with open('./result/highcited.txt', 'w') as f:
        for t in high_cited_papers:
            f.write(json.dumps(t))
            f.write('\n')
    with open('./result/latest.txt', 'w') as f:
        for t in updated_papers:
            f.write(json.dumps(t))
            f.write('\n')
