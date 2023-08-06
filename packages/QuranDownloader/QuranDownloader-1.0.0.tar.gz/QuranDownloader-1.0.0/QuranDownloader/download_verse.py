import os
import re
import requests
import grequests
from QuranDownloader.consts import *
from QuranDownloader.concurrent_req import *


url_list = []
# get info urls


def info_and_download(req_url, export_dir):
    # do info request
    info_res = concurrent_req(requests.get, req_url).json()
    print(f"reciter_name: {info_res['meta']['reciter_name']}")
    print(req_url)
    # download
    if (len(info_res['audio_files']) < 1):
        raise Exception('invalid parameters')
    for res in info_res['audio_files']:
        audio_url = res['url'].replace('//', 'https://') if (
            'mirrors' in res['url']) else f"{API_URL}/{res['url']}"
        # get audio file request
        url_list.append(concurrent_req(grequests.get, audio_url))

# download verses


def download_verse(
    reciter_name,
    verse_key=None,
    export_dir='./export',
    chapter_number=None,
    juz_number=None,
    page_number=None,
):
    # eval reciter id
    if reciter_name != 'all':
        try:
            reciter_id = RECITERS.index(reciter_name) + 1
            if not reciter_id in range(SHIKS_LIMITS[0], SHIKS_LIMITS[1]):
                raise Exception('invalid parameters')
        except:
            return print(f'{reciter_name} is not a valid reciter name\ncheck the all list from "RECITERS"')
    #
    queries = ''
    # prepare url filters
    for filter in FILTERS:
        filter_value = eval(filter)
        if (filter_value):
            queries += '?' if queries.find('?') == -1 else '&'
            queries += f'{filter}={filter_value}'
    # create export dir if not exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # do requests
    try:
        if reciter_id == 'all':
            for i in range(SHIKS_LIMITS[0], SHIKS_LIMITS[1]):
                req_url = f'{RECITATIONS_URL}/{i}{queries}'
                info_and_download(req_url, f'{export_dir}/{i}')
        else:
            req_url = f'{RECITATIONS_URL}/{reciter_id}{queries}'
            info_and_download(req_url, export_dir)
    except Exception as err:
        print(f'{err} {queries}')
    # send requests
    for file_res in concurrent_req(grequests.map, url_list):
        name = re.findall(r'\d+.mp3$', file_res.url)[0]
        # create export dir if not exists
        folder_name = re.findall(
            r'(\.com(/everyayah)?/(.+)/(?=(mp3/)?\d+.mp3))', file_res.url)
        folder_name = folder_name[0][2].replace('/', '_')
        folder_name = f'{export_dir}/{folder_name}'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # write the audio file
        open(f"{folder_name}/{name}", "wb").write(file_res.content)
