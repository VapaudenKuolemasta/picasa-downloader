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
    ACCOUNT_PREF = 'https://picasaweb.google.com/data/feed/base/user/'
    ALBUM_PREF = 'https://get.google.com/albumarchive/pwaf/'

    def __init__(self, ids, path=None):
        self.ids = ids
        self.path = path

    def download(self):
        for id in self.ids:
            url = self.ACCOUNT_PREF + id
            html = urllib.request.urlopen(url).read().decode('utf-8')

            albumIds = re.findall('<id>.*?' + id + '\/albumid\/(\d*)', html)
            if not albumIds:
                print(id + ' - No album was found in this account!')
                return

            for albumId in albumIds:
                self.filePath = os.path.join(self.path if self.path else '', id, albumId)
                os.makedirs(self.filePath, exist_ok=True)

                albumUrl = url + '/albumid/' + albumId
                html = urllib.request.urlopen(albumUrl).read().decode('utf-8')

                photoId = re.search('<id>.*?\/\d*\/albumid\/\d*\/photoid\/(\d*)', html).group(1)
                albumByPhotoUrl = self.ALBUM_PREF + id + '/album/' + albumId +'/photo/' + photoId

                self.download_album(albumByPhotoUrl)

    def download_album(self, albumUrl):
        html = urllib.request.urlopen(albumUrl).read().decode('utf-8')

        photoList = re.findall('\[\[".*?",".*?",\d*,\d*,.*?\].*?"\d{19}".*?".*?".*?"\d{9}":\[.*?[tf]\w{3,4}\]', html, re.DOTALL)
        if not photoList:
            print(albumUrl + ' - No media was found!')
            return

        pool = Pool(self.THREADS_COUNT)
        pool.map(self.download_file, photoList)
        pool.close()
        pool.join()

        print(albumUrl + ' - OK!')

    def download_file(self, photoHtml):
        photoObject = re.search('\[\[".*?","(.*?)",(\d*),(\d*),(.*?)\].*?"\d{19}".*?"(.*?)"', photoHtml, re.DOTALL)
        fileUrl = photoObject.group(1) + '=' + 'h' + photoObject.group(2) + '-w' + photoObject.group(3) + '-no'
        fileName = photoObject.group(5)

        videoUrls = re.findall('url.*?(lh3\.googleusercontent.*?m(\d\d)).*?itag', photoHtml)

        try:
            if videoUrls:
                # find biggest video
                bigSize = 0
                quality = 0

                sizes = re.findall('(\d{1,2})\/(\d*)x\d*', photoHtml)
                for size in sizes:
                    if int(size[1]) > bigSize:
                        bigSize = int(size[1])
                        quality = int(size[0])

                for videoUrl in videoUrls:
                    if int(videoUrl[1]) == quality:
                        fileUrl = 'https://' + videoUrl[0].replace('%2F','/').replace('%3D','=')
                        urllib.request.urlretrieve(fileUrl, os.path.join(self.filePath, fileName))

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
