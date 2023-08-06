
from consts import *


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
