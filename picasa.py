import argparse
import re
import os
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import time
from multiprocessing.dummy import Pool


class Picasa:
    ids = None
    path = None
    storage = None
    filePath = None

    THREADS_COUNT = 10

    def __init__(self, ids, path=None):
        self.ids = ids
        self.path = path

    def download(self):
        for id in self.ids:
            url = 'https://picasaweb.google.com/data/feed/base/user/' + id
            html = urllib.request.urlopen(url).read().decode('utf-8')

            albumList = re.findall('summary.*?'+id+'\/([\d\w]*)', html)
            if not albumList:
                print(id + ' - No album was found!')
                return

            for album in albumList:
                if album == 'albumid': continue
                self.download_albums(url + '/album/' + album)

    def download_albums(self, albumUrl):
        html = urllib.request.urlopen(albumUrl).read().decode('utf-8')

        storage = re.search('var storage = "(.*)";', html)
        if not storage:
            print(albumUrl + ' - No photo found or locked album!')
            return

        self.videoStorage = None
        self.storage = storage.group(1)
        self.securityCode = re.search('var albumSecurityCode = \"(.*)\";', html).group(1)

        links = re.findall('{(\"photoID\".*?)}', html)
        if not links:
            print(albumUrl + ' - No photo found!')
            return

        m = re.search('([\w-]+?)\.rajce\.idnes\.cz/(.*?)/', albumUrl)
        self.filePath = os.path.join(self.path if self.path else '', m.group(1), m.group(2).replace('.', '_'))
        os.makedirs(self.filePath, exist_ok=True)

        pool = Pool(self.THREADS_COUNT)
        pool.map(self.download_file, links)
        pool.close()
        pool.join()

        print(albumUrl + ' - OK!')

    def download_file(self, fileUrl):
        if re.search('\"isVideo\":(.*),\"desc', fileUrl).group(1) == 'false':
            fileName = re.search('\"fileName\":\"(.+?)\"', fileUrl).group(1)
            fileUrl = self.storage + 'images/' + fileName
        else:
            fileName = re.search('\"info\":\"(.+?\..+?)[\s\"]', fileUrl).group(1)
            photoID = re.search('\"photoID\":\"(\d+)', fileUrl).group(1)
            fileUrl = self.videoStorage + photoID

        try:
            urllib.request.urlretrieve(fileUrl, os.path.join(self.filePath, fileName))
        except urllib.error.URLError as e:
            print("Can't receive " + fileName + " '" + fileUrl + "' with " + e.reason)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ids', help="List of IDs", nargs='+', required = True)
    parser.add_argument('-p', '--path', help="Destination folder")
    # args = parser.parse_args()
    args = parser.parse_args('-i 110046880579284558208'.split())
    # args = parser.parse_args('-i http://dolfik88.rajce.idnes.cz/ -p E:/Downloads/Rajce'.split())
    downloader = Picasa(args.ids, args.path)
    downloader.download()