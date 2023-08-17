import os
import glob
import json
import shutil


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


    original_path = 'data_original/'

    splits = ['train', 'dev', 'test']


    for rev_dir in glob.glob('data_revised_*/'):
        datasetpath = os.path.join(rev_dir, 'OSPAR/')
        syn_onlypath = os.path.join(rev_dir, 'OSPAR_synthesis_text_only/')
        for split, ids in pdict.items():
            orgpath = os.path.join(os.path.join(original_path, 'OSPAR/'), split)

            paperpath = os.path.join(datasetpath, split)
            synpath = os.path.join(syn_onlypath, split)
            os.makedirs(synpath, exist_ok=True)
            for id in ids:
                fname = id + '.txt'
                org_txtfile = os.path.join(orgpath, fname)

                out_txtfile1 = os.path.join(paperpath, fname)
                shutil.copy(org_txtfile, out_txtfile1)

                out_txtfile2 = os.path.join(synpath, fname)
                shutil.copy(org_txtfile, out_txtfile2)



if __name__=='__main__':
    main()
