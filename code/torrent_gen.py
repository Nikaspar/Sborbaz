import os
from datetime import date
import torf
from torf import Torrent
from zipfile import ZipFile


def create_archive(array: set, source: str, upload_dir: str, zip_name: str):
    zip_path = os.path.join(upload_dir, zip_name)

    with ZipFile(f'{zip_path}.zip', 'a') as archive:
        for folder in array:
            try:
                archive.write(os.path.join(source, folder))
            except FileNotFoundError:
                continue


def create_torrent(archive_name: str, upload: str, torrents: str):
    try:
        t = Torrent(path=os.path.join(upload, f'{archive_name}.zip'),
                    trackers=['udp://tracker.openbittorrent.com:80/announce',
                              'udp://tracker.opentrackr.org:1337/announce'])

        t.private = True
        t.generate(threads=8)
        t.write(os.path.join(torrents, f'{archive_name}.torrent'))
    except torf.TorfError:
        pass


USERNAME = 'user'
DIRS_ARRAY = ['ABC', 'DEF', 'a']
BASE_PATH = os.path.join('A:', 'Bases')
UPLOAD_PATH = os.path.join('..', 'uploads')
ARCHIVE_NAME = '{}_{}'.format(USERNAME, date.today())
TORRENTS_PATH = os.path.join('..', 'torrents')

create_archive(set(DIRS_ARRAY), BASE_PATH, UPLOAD_PATH, ARCHIVE_NAME)
create_torrent(ARCHIVE_NAME, UPLOAD_PATH, TORRENTS_PATH)
