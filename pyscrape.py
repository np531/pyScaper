#!/usr/bin/env python3

import sys
import os
import re
import requests
import threading
import sites.w as w

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
        dumpName, imgList = w.extractImgs(url)
    else:
        raise Exception("Site type '{site}' not valid, check documentation for valid sites")

    downloadImgs(dumpName, imgList)
