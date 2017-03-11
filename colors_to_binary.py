#!/usr/bin/env python3

import json
import pickle

COLORS_1_TXT = 'data/colors_split_1.txt'
COLORS_2_TXT = 'data/colors_split_2.txt'

def colors_to_pickle(colors_file_in, pickle_file_out):
    colors = {}
    with open(colors_file_in) as f:
        for line in f:
            try:
                data = line.split('_')
                colors[data[0]] = json.loads(data[1])
                print('Read in {}...'.format(data[0]))
            except:
                continue
    with open(pickle_file_out, 'wb') as f:
        pickle.dump(colors, f)
    
if __name__ == '__main__':
    colors_to_pickle(COLORS_1_TXT, 'data/colors1.pkl')
    colors_to_pickle(COLORS_2_TXT, 'data/colors2.pkl')
