#!/bin/env python3

from shutil import unpack_archive, copy2
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
import logging
import json
import sys
import re

# ToDo: configure JSON logging handler
logging.basicConfig(level=logging.DEBUG)

base_dir = Path(__name__).parent
albums_dir = base_dir.joinpath('albums')

# The archive downloaded from Flickr consists of several ZIP files.
# *_*_partN.zip contains meta information;
# data-download-N.zip contains photos.
map = {
    'meta': base_dir.glob('*_part*.zip'),
    'photos': base_dir.glob('data-download-*.zip'),
}

# Extract meta information into a dictionary.
meta = { 'photos': {} }
is_photo = re.compile(r'photo_(\d+)\.json')
for archive in map['meta']:
    z = ZipFile(archive)
    try:
        meta['albums'] = json.loads(z.read('albums.json'))['albums']
    except KeyError:
        logging.debug(f'Missing archive.json in {archive}, trying next archive.')
    for name in z.namelist():
        if not is_photo.match(name):
            logging.debug(f'Skipping {name}.')
            continue
        photo_id = is_photo.sub(r'\1', name)
        meta['photos'][photo_id] = json.loads(z.read(name))
if not 'albums' in meta:
    logging.error(f'Archive does not contain albums.json, unable to restore albums, aborting.')
    sys.exit(2)

# Extract photos into a temporary folder.
# Move photos into album folders.
title_re = re.compile(r'[/\?\* ,:]+')
with TemporaryDirectory() as tmp_dir:
    photos_dir = Path(tmp_dir)
    for archive in map['photos']:
        logging.debug(f'Unpacking {archive} into {tmp_dir}.')
        unpack_archive(archive, photos_dir)
    for a in meta['albums']:
        logging.info(f'Processing album: {a["title"]}, {a["photo_count"]} photos.')
        # Normalize the album title before using as a directory name,
        # i.e. replace special characters with underscore.
        title_norm = title_re.sub('_', a['title'])
        album_dir = albums_dir.joinpath(f"Flickr_{title_norm}")
        album_dir.mkdir(exist_ok=True,parents=True)
        # Iterate and copy photos to album directory.
        for p in a['photos']:
            if not p in meta['photos']:
                logging.warning(f"Photo {p} from album {a['title']} does not exist, skipping.")
                continue
            photo = meta['photos'][p]
            # The photo['id'] is contained in the name of a photo,
            # e.g. photos/dsc_7264_<ID>_o.jpg.
            # Finding the photo requires globbing;
            # error out and skip, if glob returns more then one photo.
            p_id = photo["id"]
            photo_candidates = list(photos_dir.glob(f'*{p_id}*'))
            if len(photo_candidates) == 0:
                logging.warning(f"Could not find photo with ID {p_id}, skipping.")
                continue
            if len(photo_candidates) > 1:
                logging.warning(f"Multiple photos matched ID {p_id}, don't know what to do, skipping.")
                continue
            photo_path = photo_candidates[0]
            logging.debug(f'Copying {photo_path} to {album_dir}.')
            copy2(photo_path, album_dir)
