# -*- coding: utf-8 -*-
'''
    Decode vk mp3 url
'''
import json
import sys
import re
import os

import requests
import decode
if sys.version_info > (3, 0):
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser


helptext = """
Tool for get link to download mp3 files
    from playlist in the russian social network vk.com.
    Output - bash script.

Usage:
    {prog_name} [option]

    Options:
        update            - update playlist (save in playlist_file)
        info              - show song count (in playlist_file)
        info name         - list all song name and position number
        position [number] - get 10 link to songs
        save              - create template config.json
        help, --help, -h  - view this text
"""

config_file = 'config.json'

owner_id = ''

owner_cookies = {'Cookie': 'remixlang=3;'
                 + 'remixstid=<FILL>; '
                 + 'remixflash=0.0.0; remixscreen_depth=24; remixdt=0;'
                 + 'remixsid=<FILL>; '
                 + 'remixrefkey=<FILL>; '
                 + 'remixcurr_audio=<FILL>'}

playlist_file = 'dump.json'

useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 \
Firefox/63.0'

ALLOW_SYMBOLS = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCV\
BNMйцукеёнгшщзхъфывапролджэячсмитьбюЙЦУКЕЁНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТ\
ЬБЮ .,-()1234567890'


def getAllowName(string):
    s = ''
    st = string.lower()
    global ALLOW_SYMBOLS
    for x in st[:125]:
        if x in ALLOW_SYMBOLS:
            s += x
    return s


def ids_10_url_row(data):
    song_col = len(data["list"])
    cnt = 0
    delim1 = ","
    delim2 = ""
    result = ""
    while (cnt < song_col):
        if cnt % 10 == 0:
            result += delim2 + str(data["list"][cnt][1]) + \
                "_" + str(data["list"][cnt][0])
            delim2 = "\n"
        else:
            result += delim1 + str(data["list"][cnt][1]) + \
                "_" + str(data["list"][cnt][0])
        cnt += 1
    return result


def cut_trash(text, pattern):
    vtmp = re.findall(pattern, text)
    data = json.loads(''.join(vtmp[0]))
    return data


def request_data_vk(payload):
    vk_headers = {'Host': 'vk.com',
                  'User-Agent': useragent,
                  'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'https://vk.com/audios' + owner_id,
                  'DNT': '1',
                  'Connection': 'keep-alive'}
    vk_headers.update(owner_cookies)
    r = requests.post('https://vk.com/al_audio.php',
                      data=payload, headers=vk_headers)
    return r


def save_config():
    data = {}
    data.update({'owner_id': owner_id})
    data.update({'owner_cookies': owner_cookies})
    data.update({'playlist_file': playlist_file})
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    print('config.json created')


def load_config():
    with open(config_file, 'r') as conf_file:
        data = json.load(conf_file)
        global owner_id
        global owner_cookies
        global playlist_file
        owner_id = data['owner_id']
        owner_cookies = data['owner_cookies']
        playlist_file = data['playlist_file']


if __name__ == '__main__':

    # help
    if ("help" in sys.argv or "--help" in sys.argv or "-h" in sys.argv or
            (len(sys.argv) < 2)):
        print(helptext.format(prog_name=sys.argv[0]))
        exit()

    # save config
    if "save" in sys.argv:
        save_config()
        exit()

    if os.path.isfile(config_file):
        load_config()
    else:
        save_config()

    # wrong config
    if not owner_id:
        print('Empty owner_id\n Check config.json')
        exit()

    # info
    if os.path.isfile(playlist_file) and ("info" in sys.argv):
        with open(playlist_file, 'r') as json_file:
            data = json_file.read()
        data = json.loads(data)
        print("# Current song: " + str(data[0]["totalCount"]))
        parser = HTMLParser()
        if "name" in sys.argv:
            parser = HTMLParser()
            cnt = 0
            for i in data:
                for line in i["list"]:
                    print(str(cnt // 10) + "\t" +
                          ' '.join(parser.unescape(line[4] + " - " + line[3]).
                                   split()))
                    cnt += 1
        exit()

    # update
    if not(os.path.isfile(playlist_file)) or ("update" in sys.argv):
        print("# Create/update playlist_file!")
        hasMore = 1
        data = []
        temp = []
        nextOffset = "0"
        payload = {'access_hash': '', 'act': 'load_section', 'al': '1',
                   'claim': '0', 'offset': '1', 'owner_id': owner_id,
                   'playlist_id': '-1', 'type': 'playlist'}

        while (hasMore == 1):
            payload['offset'] = nextOffset
            temp = request_data_vk(payload)
            temp = cut_trash(temp.text, r'{.*}')
            nextOffset = temp["nextOffset"]
            hasMore = temp["hasMore"]
            data.append(temp)
        with open(playlist_file, "w") as save_file:
            json.dump(data, save_file)
    else:
        print("# File playlist_file exist!")
        with open(playlist_file, 'r') as json_file:
            data = json_file.read()
        data = json.loads(data)

    # output data.json
    parser = HTMLParser()
    cnt = 0
    for i in data:
        for line in i["list"]:
            if line[2]:
                sys.stdout.write(
                    "ffmpeg -i " +
                    "'" +
                    (decode.decode(line[2], line[1]) if decode.check(
                        line[2]) else line[2]) +
                    "'" +
                    " -codec copy " +
                    "'" +
                    ' '.join(
                        getAllowName(
                            parser.unescape(line[4] + " - " + line[3])
                        ).split()) + ".mp3" +
                    "'" +
                    "\n")
                cnt += 1
