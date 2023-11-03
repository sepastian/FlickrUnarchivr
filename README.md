# FlickrUnarchivr

Restore albums from a Flickr data request.

A Flickr data request does not retain albums, as shown on Flickr. The information about albums is contained in JSON files. This scripts restores your albums, generating one folder per album, placing all photos and video belonging to an album inside the album folder.

FlickrUnarchivr uses Python 3, to efficiently handle archive files, parse JSON data, create folders and move media files around.

## Installation and Usage

Clone this repository, place the ZIP files comprising your Flickr data request in the project directory, run the `restore.py` script. Make sure you have Python 3 installed. No external libraries are required.

```shell
$ git clone git@github.com:sepastian/FlickrUnarchivr.git
$ cd FlickrUnarchivr

# Assuming flickr data request files
# have been downloaded to Downloads/.
$ cp ~/Downloads/FlickrDataRequest/* . 

# ZIP file are in place:
$ ls
README.md
restore.py
72157722185468047_06fxe76mos37_part1.zip
data-download-1.zip
data-download-2.zip
data-download-3.zip

# Restore albums into ./albums/.
python3 ./restore.py
```

You will now find restored albums in the `./albums` folder.

## How Do I Get My Flickr Data?

Login to Flickr, go to Profile picture > Account & Subscriptions > Your Flickr Data, request your data. You will receive an email notification when your data request has been processed. After receiving the notification, download all ZIP files, i.e. "account data" and "photos and videos".
