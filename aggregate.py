#!/usr/bin/env python3

from datetime import datetime
from PIL import Image
from multiprocessing import cpu_count
from subprocess import Popen, PIPE

import csv
import io
import json
import threading
import os

NUM_THREADS = cpu_count()
WEBSITE_CSV = 'top_500_domains.csv'
COLORS_TXT = 'colors.txt'

def chunks(l, chunks):
    """
    Given a list and an integer n, this splits the list in n evenly sized
    chunks.
    """
    return [l[i::chunks] for i in range(chunks)]

def get_screenshot_command(url, logfile):
    """
    Given a url and a logfile name, this function formats the webkit2png
    command for passing into Popen.
    """
    return ['webkit2png', 'https://{}'.format(url),
            '--log={}'.format(logfile), '--feature=javascript']

def get_image(url, logfile):
    """
    Given a url and a logfile name, this function runs the webkit2png
    script on the url and returns a PIL Image object containing a
    screenshot of the webpage.
    """
    try:
        os.unlink(logfile)
    except:
        pass
    command = Popen(get_screenshot_command(url, logfile),
                    stdout=PIPE, stderr=PIPE)
    output, error = command.communicate()
    with open(logfile) as log:
        data = log.read()
        print(data)
        if 'Failed to load' in data:
            return None
    try:
        return Image.open(io.BytesIO(output))
    except:
        return None

def write_image_data(url, logfile):
    """
    Given a url and a logfile name, this fetches a screenshot of the
    webpage at the url and writes its color data to a designated CSV file.
    It returns the time needed to execute the image fetching and writing.
    """
    start = datetime.now()
    image = get_image(url, logfile)
    if image is None:
        return 0
    width, height = image.size
    colors = sorted(image.getcolors(width * height), key=lambda x: x[0])
    with open(COLORS_TXT, 'a') as f:
        f.write('{}_{}\n'.format(url, json.dumps(colors)))
    end = datetime.now()
    return (end - start).total_seconds()

class AggregatorThread(threading.Thread):
    """
    This class allows us to do the image fetching in a thread so
    that we can fetch screenshot data faster.
    """

    def __init__(self, id, urls):
        threading.Thread.__init__(self)
        self.id = id
        self.logfile = 'thread{}.tmp.log'.format(self.id)
        self.urls = urls

    def run(self):
        print('THREAD {} STARTED'.format(self.id))
        for url in self.urls:
            timedelta = write_image_data(url, self.logfile)
            print('THREAD {}: Fetched {} in {}s'.format(self.id, url, timedelta))
        print('THREAD {} COMPLETED'.format(self.id))

def get_urls():
    """
    This method fetches the urls to screenshot from a CSV of domains
    """
    with open(WEBSITE_CSV) as f:
        data = f.read().strip().split('\n')[1:]
    return list(map(lambda field: field.split(',')[1].strip('"'), data))

def aggregate():
    """
    This is a single threaded aggregation method for fetching website
    screenshot color data.
    """
    for url in get_urls():
        timedelta = write_image_data(url, 'tmp.log')
        print('Fetched {} in {}s'.format(url, timedelta))

def threaded_aggregate():
    """
    This method uses multithreading to fetch website screenshot color
    data.
    """
    urls = chunks(get_urls(), NUM_THREADS)
    threads = []
    for i in range(NUM_THREADS):
        threads.append(AggregatorThread(i, urls[i]))
    for i in range(NUM_THREADS):
        threads[i].start()
    for i in range(NUM_THREADS):
        threads[i].join()
        
if __name__ == '__main__':
    threaded_aggregate()
