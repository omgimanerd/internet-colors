#!/usr/bin/env python3

from datetime import datetime
from PIL import Image
from util import chunk

import contextlib
import io
import json
import logging
import subprocess
import threading
import os

log = logging.getLogger('aggregate')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(logging.Formatter("%(threadName)s %(message)s"))
log.setLevel(logging.DEBUG)
log.addHandler(streamHandler)

NUM_THREADS = 8
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
    with contextlib.suppress(FileNotFoundError):
        os.remove(logfile)
    output = subprocess.run(get_screenshot_command(url, logfile),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE).stdout
    with open(logfile) as log:
        data = log.read()
        if "Failed to load" in data:
            return None
    with contextlib.suppress(OSError):
        return Image.open(io.BytesIO(output))


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
        data = f.read().splitlines()[1:]
    return [field.split(',')[1].strip('\"') for field in data]


def aggregate(urls, logfile):
    """
    This is a single threaded aggregation method for fetching website
    screenshot color data. We can call this with all the urls to do
    the aggregation with a single thread, or we can split the urls
    into chunks to do this with multi-threading
    """
    # From waflores
    # Protip - you can actually get logging to give you TID for free
    # https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
    log.debug("started")
    for url in urls:
        result = write_image_data(url, logfile)
        log.debug(result["message"])
    log.debug("completed")


def threaded_aggregate():
    """
    This method uses multithreading to fetch website screenshot color
    data.
    """
    urls = chunk(get_urls(), NUM_THREADS)
    logfiles = ["Thread{}.tmp.log".format(i) for i in range(NUM_THREADS)]
    threads = [threading.Thread(
        target=aggregate,
        args=(urls[i], logfiles[i])) for i in range(NUM_THREADS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    with contextlib.suppress(FileNotFoundError):
        [os.remove(logfile) for logfile in logfiles]


if __name__ == "__main__":
    threaded_aggregate()
