import re
import os
import requests
import grequests
import concurrent.futures
from verse_key_converters import verse_key_to_num


def word_spreader(label):
    # remove tajweed hokm in between words
    label = re.sub('<tajweed class=\w+>(\w* \w*)<\/tajweed>', '\g<1>', label)
    # split at any word space
    return re.split('(?<!tajweed) ', label)
# make concurrent requests


def concurrent_req(fun, url):
    executor = concurrent.futures.ProcessPoolExecutor()
    future = executor.submit(fun, url)
    return future.result()

# download word audio file


def download_word(verse_key, export_dir='./export/words'):
    quran_req = concurrent_req(
        requests.get, f'https://api.quran.com/api/v4/quran/verses/imlaei?verse_key=1:3').json()
    # try to get the verse
    try:
        quran_data = quran_req['verses'][0]['text_imlaei']
    except:
        return print('{verse_key} is not a valid verse key')
    # loop throw all word to fill the requests
    url = 'https://verses.quran.com/wbw/{}.mp3'
    url_list = []
    for i, word in enumerate(quran_data.split(' ')):
        word_key = f"{verse_key}:{i + 1}"
        link = url.format(verse_key_to_num(word_key))
        url_list.append(grequests.get(link))
    # create export dir if not exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # request
    for file_res in concurrent_req(grequests.map, url_list):
        name = file_res.url.split('/')[-1]
        open(f"{export_dir}/{name}", "wb").write(file_res.content)
