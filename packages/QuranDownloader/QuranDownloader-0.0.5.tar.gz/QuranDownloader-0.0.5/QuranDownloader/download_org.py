import grequests
import requests
import re
import os
import json
# from Spreader import word_spreader
# from convert_all_mono_to_wav import verse_key_to_num
# verse key converters

RECITERS = ['AbdulBaset_Mujawwad', 'AbdulBaset_Murattal', 'Sudais', 'Shatri', 'Rifai', 'Husary',
            'Alafasy', 'Minshawi_Mujawwad', 'Minshawi_Murattal', 'Shuraym', 'Mohammad_al_Tablaway', 'Husary_Muallim']
SHIKS_LIMITS = [1, 13]

def verse_key_to_num(verse_key, sep=':'):
    all_ids = []
    for num in verse_key.split(sep):
        all_ids.append(f'{int(num):03}')
    return '_'.join(all_ids)


def num_to_verse_key(num, sep='-'):
    verse_num = re.findall('\d{3}', num)
    verse_num = [int(v) for v in verse_num]
    return sep.join(verse_num)

# quran_data = requests.get('https://api.quran.com/api/v4/quran/verses/uthmani').json()
# print(quran_data)


def word_spreader(label):
    # remove tajweed hokm in between words
    label = re.sub('<tajweed class=\w+>(\w* \w*)<\/tajweed>', '\g<1>', label)
    # split at any word space
    return re.split('(?<!tajweed) ', label)


filters = ['chapter_number', 'juz_number', 'page_number', 'verse_key']
file_url = 'https://verses.quran.com'
# do action and download

url_list = []


def info_and_download(req_url, export_dir):
    # do info request
    info_res = requests.get(req_url).json()
    print(f"reciter_name: {info_res['meta']['reciter_name']}")
    print(req_url)
    # download
    for res in info_res['audio_files']:
        audio_url = res['url'].replace('//', 'https://') if (
            'mirrors' in res['url']) else f"{file_url}/{res['url']}"
        # print(audio_url)
        # get audio file request
        url_list.append(grequests.get(audio_url))
        # file_res = requests.get(audio_url)


def download(
    reciter_name,
    export_dir='./export',
    chapter_number=None,
    juz_number=None,
    page_number=None,
    verse_key=None
):
    # eval reciter id
    if reciter_name != 'all':
        try:
            reciter_id = RECITERS.index(reciter_name) + 1
            if not reciter_id in range(SHIKS_LIMITS[0], SHIKS_LIMITS[1]): raise Exception()
        except:
            return print(f'{reciter_name} is not a valid reciter name\ncheck the all list from "RECITERS"')
    # 
    queries = ''
    # prepare url filters
    for filter in filters:
        filter_value = eval(filter)
        if (filter_value):
            queries += '?' if queries.find('?') == -1 else '&'
            queries += f'{filter}={filter_value}'
    print(queries)
    # create export dir if not exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # do requests
    if reciter_id == 'all':
        for i in range(SHIKS_LIMITS[0], SHIKS_LIMITS[1]):
            req_url = f'https://api.quran.com/api/v4/quran/recitations/{i}{queries}'
            info_and_download(req_url, f'{export_dir}/{i}')
    else:
        req_url = f'https://api.quran.com/api/v4/quran/recitations/{reciter_id}{queries}'
        info_and_download(req_url, export_dir)
    print(req_url)
    # send requests
    for file_res in grequests.imap(url_list):
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

# download word audio file


def download_word(string_text='text_uthmani', from_verse=0, verses_count=None,  export_dir='./export/words'):
    quran_data = requests.get(
        'https://api.quran.com/api/v4/quran/verses/uthmani').json()
    url = 'https://verses.quran.com/wbw/{}.mp3'
    url_list = []
    for verse in quran_data['verses'][from_verse:verses_count]:
        word_spreaded = word_spreader(verse[string_text])
        for i, word in enumerate(word_spreaded):
            word_key = f"{verse['verse_key']}:{i + 1}"
            link = url.format(verse_key_to_num(word_key))
            url_list.append(grequests.get(link))
    # create export dir if not exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # request
    for file_res in grequests.imap(url_list):
        name = file_res.url.split('/')[-1]
        open(f"{export_dir}/{name}", "wb").write(file_res.content)
