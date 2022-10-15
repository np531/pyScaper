import requests
import uuid
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
    try:
        title = soup.find(class_="post op").find(class_="nameBlock").contents[2].contents[0]
    except IndexError:
        title = str(uuid.uuid4())

    for fileTag in soup.find_all(class_="fileText"):
        imgSrc = fileTag.find('a').get('href')[2:]
        name = fileTag.find('a').contents[0]
        urlList.append((name, imgSrc))
    return title, urlList
