#!/usr/bin/python

from multiprocessing import Pool
import time

def f(x):
    # time.sleep(3)
    return x * x

if __name__ == '__main__':
    p = Pool(8)
    # a = list(map(f, range(9999999)))
    a = p.map(f, range(9999999))
    
