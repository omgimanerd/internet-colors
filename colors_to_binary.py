#!/usr/bin/env python3

import json
import pickle

COLORS_TXT = 'colors.txt'

def colors_to_pickle(pickle_file_out):
    colors = {}
    with open(COLORS_TXT) as f:
        for line in f:
            try:
                data = line.split('_')
                colors[data[0]] = json.loads(data[1])
                print('Read in {}...'.format(data[0]))
            except:
                continue
    with open(pickle_file_out, 'w') as f:
        pickle.dump(colors, f)
    
if __name__ == '__main__':
    colors_to_pickle('colors.bin')
