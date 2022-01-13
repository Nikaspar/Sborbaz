import os
import torf
from datetime import date
from shutil import copytree
from torf import Torrent


def get_folders(array: set, source: str, destination: str, name: str):
    for folder in array:
        if os.path.exists(os.path.join(source, folder)):
            print('Copy "{}" to "{}{}{}"'.format(folder, destination, os.sep, name))
        try:
            copytree(os.path.join(source, folder), os.path.join(destination, name, folder))
        except FileNotFoundError:
            print(f'[warn]Folder "{folder}" not fount. Continue\n')
            continue
        except FileExistsError:
            print(f'[warn]Folder "{folder}" already exists. Continue\n')
            continue
        else:
            print('Copy is done\n')


def create_torrent(upload: str, name: str, torrents: str):
    try:
        print('Torrent file is being created')
        t = Torrent(path=os.path.join(upload, f'{name}'),
                    trackers=['udp://tracker.openbittorrent.com:80/announce',
                              'udp://tracker.opentrackr.org:1337/announce'])

        t.private = True
        t.generate(threads=8)
        t.write(os.path.join(torrents, f'{name}.torrent'))
    except torf.TorfError as ex:
        print(f'[warn] {ex}\n')
        pass
    else:
        print('Torrent file created\n')
    print('All done')


USERNAME = input('username:\n>>> ')  # 'user'
DIRS_ARRAY = open('baselist.txt').read().split()  # ['ABC', 'DEF', 'a']
BASE_PATH = os.path.join('A:', 'Bases')
UPLOAD_PATH = os.path.join('..', 'uploads')
UPLOAD_NAME = '{}_{}'.format(USERNAME, date.today())
TORRENTS_PATH = os.path.join('..', 'torrents')

get_folders(set(DIRS_ARRAY), BASE_PATH, UPLOAD_PATH, UPLOAD_NAME)
create_torrent(UPLOAD_PATH, UPLOAD_NAME, TORRENTS_PATH)
