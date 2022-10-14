#!/usr/bin/env python3

import requests
import sys
import os
import re
import threading
from bs4 import BeautifulSoup as bs

def extractImgs(url):
    """
    Given a target thread, extracts the full scale image source
    for each image in the thread.
    Args: url of target thread
    Returns: a list of img sources
    """
    urlList = []
    soup = bs(requests.get(url).text, features='html.parser')

    # Grab title of thread 
    title = soup.find(class_="post op").find(class_="nameBlock").contents[2].contents[0]

    for fileTag in soup.find_all(class_="fileText"):
        imgSrc = fileTag.find('a').get('href')[2:]
        name = fileTag.find('a').contents[0] 
        urlList.append((name, imgSrc))
    return title, urlList 


def pullImg(dumpFolder, imgTup):
    img = requests.get('https://' + imgTup[1])
    print(imgTup)
    with open(dumpFolder + '/' + imgTup[0], "wb+") as f:
        f.write(img.content)


def downloadImgs(dumpName, imgList):
    dumpFolder = targetDir + '/' + dumpName

    if imgList and not os.path.exists(dumpFolder):
        os.mkdir(dumpFolder)

    threadList = []
    for imgTup in imgList:
        newThread = threading.Thread(name = f"thread{len(threadList)}", target = pullImg, args = (dumpFolder, imgTup), daemon = False)
        threadList.append(newThread.name)
        newThread.start()


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        raise Exception(f"Usage: {sys.argv[0]} <site> <url> <target dir>")
    site = sys.argv[1]
    url = sys.argv[2]
    targetDir = sys.argv[3]

    if not os.path.exists(targetDir):
        raise Exception(f"The provided directory '{targetDir}' does not exist")

    title = 'Pyscrape - Thread Image Scapper v1'
    print('='*len(title))
    print(title)
    print('='*len(title))
    print()

    if site == 'w': 
        dumpName, imgList = extractImgs(url)
    else:
        raise Exception("Site type '{site}' not valid, check documentation for valid sites")

    downloadImgs(dumpName, imgList)
