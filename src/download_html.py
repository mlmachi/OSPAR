import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup

def get_text(soup):
    for s in soup.find_all('div', class_='figcaption'):
        s.decompose()

    steps = soup.find_all(class_='step')
    raw_text = steps[0].text
    text = modify_text(raw_text)

    return text


def modify_text(text, rm_notes=True, rm_figures=True):
    texts = []

    for line in text.split('\n'):
        if re.search('[\w\$\.\,]', line):
            # remove excess space characters
            line = re.sub('\s{1,10}', ' ', line)
            if len(line) < 1:
                continue
            if line[0] == ' ':
                line = line[1:]
            if line[-1] == ' ':
                line = line[:-1]
            texts.append(line)

    ret_text = ' '.join(texts)
    ret_text = re.sub(' \,', ',', ret_text)
    ret_text = re.sub(' \.', '.', ret_text)
    ret_text = re.sub(' \n', '\n', ret_text)
    ret_text = re.sub('\( ', '(', ret_text)
    ret_text = re.sub(' \)', ')', ret_text)
    if rm_notes:
        text = ''
        while 1:
            text = re.sub('(\(Note[^\(\)]+)\([^\(\)]+\)', r'\1', ret_text)
            if text == ret_text:
                break
            else:
                ret_text = text
        ret_text = re.sub('\(Note[^\)]+\)', '', ret_text)
        ret_text = re.sub('\s{1,3}', ' ', ret_text)
        ret_text = re.sub(' \,', ',', ret_text)
        ret_text = re.sub(' \.', '.', ret_text)
        ret_text = re.sub('\,\,', ',', ret_text)
        ret_text = re.sub('\,\.', '.', ret_text)
        ret_text = re.sub('\.\.', '.', ret_text)
        ret_text = re.sub('\, and\.', '.', ret_text)
        ret_text = re.sub('\( and \)', '', ret_text)

    if rm_figures:
        text = ''
        while 1:
            text = re.sub('(\(Figure[^\(\)]+)\([^\(\)]+\)', r'\1', ret_text)
            if text == ret_text:
                break
            else:
                ret_text = text

        ret_text = re.sub('\(Figure[^\)]*\)', '', ret_text)
        ret_text = re.sub('\s{1,3}', ' ', ret_text)
        ret_text = re.sub(' \,', ',', ret_text)
        ret_text = re.sub(' \.', '.', ret_text)
        ret_text = re.sub('\,\,', ',', ret_text)
        ret_text = re.sub('\,\.', '.', ret_text)
        ret_text = re.sub('\.\.', '.', ret_text)
        ret_text = re.sub('\, and\.', '.', ret_text)
        ret_text = re.sub('\( and \)', '', ret_text)


    return ret_text

def read_ann(annfile):
    with open(annfile, 'r') as lines:
        for line in lines:
            items = line.strip().split('\t')
            if items[0][0] == 'T':
                label, start, end = items[1].split(' ')
                if label == 'B_Workup':
                    wu_idx = int(start)
                    break

    return wu_idx

def main():
    ids = []
    with open('corpus_papers.json', 'r') as f:
        pdict = json.load(f)

    urlpath = 'http://www.orgsyn.org/demo.aspx?prep='
    datasetpath = 'data_original/OSPAR/'
    syn_onlypath = 'data_original/OSPAR_synthesis_text_only/'

    c = 1
    print('Downloading and text processing.')
    print('This takes about 20 min.')
    for split, ids in pdict.items():
        paperpath = os.path.join(datasetpath, split)
        synpath = os.path.join(syn_onlypath, split)
        os.makedirs(synpath, exist_ok=True)
        for id in ids:
            print(str(c) + '/112 ' + id)
            c += 1
            try:
                html = requests.get(urlpath + id)
                soup = BeautifulSoup(html.text, 'html.parser')

                all_text = get_text(soup)

                with open(os.path.join(paperpath, id + '.txt'), 'w') as f:
                    f.write(all_text)

                wu_idx = read_ann(os.path.join(paperpath, id + '.ann'))
                syn_text = all_text[:wu_idx]

                with open(os.path.join(synpath, id + '.txt'), 'w') as f:
                    f.write(syn_text)


                time.sleep(10)

            except requests.exceptions.RequestException as err:
                print(err)

    print('Completed.')


if __name__=='__main__':
    main()
