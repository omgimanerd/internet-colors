#!/usr/bin/env python3

from datetime import datetime
from PIL import Image
from multiprocessing import cpu_count
from subprocess import Popen, PIPE

from util import chunk

import io
import json
import threading
import os

NUM_THREADS = cpu_count()
WEBSITE_CSV = "data/top_500_domains.csv"
COLORS_FILE = "data/colors.txt"
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
TIMEOUT_DURATION = 60

def get_screenshot_command(url, logfile):
    """
    Given a url and a logfile name, this function formats the webkit2png
    command for passing into Popen.
    """
    return ["webkit2png",
            "https://{}".format(url),
            "--log={}".format(logfile),
            "--feature=javascript",
            "-g", str(IMAGE_WIDTH), str(IMAGE_HEIGHT),
            "--timeout={}".format(TIMEOUT_DURATION)]

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
        if "Failed to load" in data:
            return None
    try:
        return Image.open(io.BytesIO(output))
    except:
        return None

def write_image_data(url, logfile):
    """
    Given a url and a logfile name, this fetches a screenshot of the
    webpage at the url and writes its color data to a designated CSV file.
    It returns a success status containing a debug message.
    """
    start = datetime.now()
    image = get_image(url, logfile)
    if image is None:
        return {
            "success": False,
            "message": "{} did not return a valid image".format(url)
        }
    width, height = image.size
    colors = sorted(image.getcolors(width * height), key=lambda x: x[0])
    with open(COLORS_FILE, "a") as f:
        f.write("{}_{}\n".format(url, json.dumps(colors)))
    end = datetime.now()
    return {
        "success": True,
        "message": "Fetched {} ({}x{}) in {}".format(
            url, width, height, (end - start).total_seconds())
    }

def get_urls():
    """
    This method fetches the urls to screenshot from a CSV of domains
    """
    with open(WEBSITE_CSV) as f:
        data = f.read().strip().split("\n")[1:]
    return list(map(lambda field: field.split(",")[1].strip("\""), data))

def aggregate(urls):
    """
    This is a single threaded aggregation method for fetching website
    screenshot color data. We can call this with all the urls to do
    the aggregation with a single thread, or we can split the urls
    into chunks to do this with multi-threading
    """
    name = threading.currentThread().getName()
    print("THREAD {} STARTED".format(name))
    logfile = "{}.tmp.log".format(name)
    for url in urls:
        result = write_image_data(url, logfile)
        print("THREAD {}: {}".format(name, result["message"]))
    print("THREAD {} COMPLETED".format(name))

def threaded_aggregate():
    """
    This method uses multithreading to fetch website screenshot color
    data.
    """
    urls = chunk(get_urls(), NUM_THREADS)
    threads = [threading.Thread(
        target=aggregate, args=(urls[i],)) for i in range(NUM_THREADS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == "__main__":
    threaded_aggregate()
