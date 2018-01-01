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
                self.filePath = os.path.join(self.path if self.path else '', id, album)
                os.makedirs(self.filePath, exist_ok=True)
                self.download_albums(url + '/album/' + album)

    def download_albums(self, albumUrl):
        html = urllib.request.urlopen(albumUrl).read().decode('utf-8')

        entryList = re.findall('<entry>(.*?)<\/entry>', html)
        if not entryList:
            print(albumUrl + ' - No media was found!')
            return

        pool = Pool(self.THREADS_COUNT)
        pool.map(self.download_entry, entryList)
        pool.close()
        pool.join()

        print(albumUrl + ' - OK!')

    def download_entry(self, entry):
        urlList = re.findall('<media:content url=\'(.*?)\'', entry)
        if not urlList:
            print('No media in current entry!')
            return

        fileName = ''
        videoSize = 0
        fileUrl = ''
        for url in urlList:
            name = re.search('.*/(.*?)$', url).group(1)

            if name.find("=") == -1:
                fileName = name
                fileUrl = url if fileUrl == '' else fileUrl
                continue

            if re.search('=m(\d+)', url) and int(re.search('=m(\d+)', url).group(1)) > videoSize:
                fileUrl = url

        try:
            urllib.request.urlretrieve(fileUrl, os.path.join(self.filePath, fileName))
        except urllib.error.URLError as e:
            print("Can't receive " + fileName + " '" + fileUrl + "' with " + e.reason)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ids', help="List of IDs", nargs='+', required=True)
    parser.add_argument('-p', '--path', help="Destination folder")
    args = parser.parse_args()
    downloader = Picasa(args.ids, args.path)
    downloader.download()
