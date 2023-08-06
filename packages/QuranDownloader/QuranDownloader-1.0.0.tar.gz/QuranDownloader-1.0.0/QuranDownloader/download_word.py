import re
import os
import requests
import grequests
from QuranDownloader.verse_key_converters import verse_key_to_num
from QuranDownloader.concurrent_req import *


def word_spreader(label):
    # remove tajweed hokm in between words
    label = re.sub('<tajweed class=\w+>(\w* \w*)<\/tajweed>', '\g<1>', label)
    # split at any word space
    return re.split('(?<!tajweed) ', label)

# download word audio file


url = 'https://verses.quran.com/wbw/{}.mp3'


def download_word(verses_keys, export_dir='./export/words'):
    url_list = []
    for verse_key in verses_keys:
        quran_req = concurrent_req(
            requests.get, f'https://api.quran.com/api/v4/quran/verses/imlaei?verse_key={verse_key}').json()
        # try to get the verse
        try:
            quran_data = quran_req['verses'][0]['text_imlaei']
        except:
            return print('{verse_key} is not a valid verse key')
        # loop throw all word to fill the requests
        for i, word in enumerate(quran_data.split(' ')):
            word_key = f"{verse_key}:{i + 1}"
            link = url.format(verse_key_to_num(word_key))
            url_list.append(grequests.get(link))
    # create export dir if not exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # do requests
    for file_res in concurrent_req(grequests.map, url_list):
        name = file_res.url.split('/')[-1]
        open(f"{export_dir}/{name}", "wb").write(file_res.content)
