# Rajce Downloader
Command line script for download albums with photos and videos from rajce.idnes.cz. 
Will create a folder named after author and subfolder named after album for this. For example, for url 

    https://author.rajce.idnes.cz/albumName
new path will look like

    D:\Destination Folder\author\albumName

## Requirements
* [Python 3.6.1+](https://www.python.org/downloads)

## Options
    -h, --help                            Show this help message and exit
    -u URL [URL ...], --url URL [URL ...] List of URLs
    -p PATH, --path PATH                  Destination folder
    
## Examples
    rajce.py -u URL [URL ...] [-p PATH]

You can set only specific album

    rajce.py -u https://author.rajce.idnes.cz/albumName
Or with destination folder

    rajce.py -u https://author.rajce.idnes.cz/albumName -p E:\Downloads\Rajce
Or download all albums of one author

    rajce.py -u https://author.rajce.idnes.cz/
Or all albums of few authors separeted by space

    rajce.py -u https://authorOne.rajce.idnes.cz/ https://authorTwo.rajce.idnes.cz/
    
Or all albums of one author and only one album of other and set destination folder. You get the idea, i think.
