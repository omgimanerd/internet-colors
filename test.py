#!/usr/bin/python

from multiprocessing import Pool
import time

def f(n):
    return n ** 2

# function to be mapped over
def calculateParallel(numbers, threads=2):
    pool = Pool(threads)
    results = pool.map(f, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers = list(range(9999999))
    # for i in range(9999999):
    #     numbers[i] = f(numbers[i])
    squaredNumbers = calculateParallel(numbers, 8)
