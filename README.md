# Picasa Downloader
Download photo and video from google photohosting using google ID. (picasa, plus.google, albumarchive)

## Requirements
* [Python 3.6.1+](https://www.python.org/downloads)

## Options
    -h, --help                        Show this help message and exit
    -i ID [ID ...], --ids ID [ID ...] List of URLs
    -p PATH, --path PATH              Destination folder
    
## Examples
    picasa.py -i GoogleID [GoogleID ...] [-p PATH]

You can set only specific google account

    picasa.py -i 123123123123123123123
Or with destination folder

    picasa.py -i 123123123123123123123 -p E:\Downloads\Picasa
Or few google accounts separeted by space

    picasa.py -i 123123123123123123123 456456456456456456456
    