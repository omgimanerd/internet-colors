#!/usr/bin/env python3

import json

if __name__ == '__main__':
    with open('data/colors.txt') as f:
        for line in f:
            colors = json.loads(line.split('_')[1])
            total = 0
            for entry in colors:
                total += entry[0]
            print(total)
