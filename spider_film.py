# -*- coding: utf-8 -*-
"""
Created on Tue May 28 20:47:49 2019

@author: a3139
"""

import re
import requests
import json
import time
from multiprocessing import Pool
from requests.exceptions import RequestException

def read_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?src="(http.*?)".*?</a>'
                         + '.*?name">.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?'
                         + 'integer">(.*?)</i>.*?fraction">(.*?)</i>'
                         + '.*?</dd>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield{
                'index':item[0],
                'image':item[1],
                'film_name':item[2],
                'actors':item[3].strip()[3:],
                'rele_time':item[4][5:15],
                'score':item[5]+item[6]
                    }

def write_to_file(content):
    with open('Top_100_Films.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = read_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(1)
    ''' pool太快，数据容易丢失
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])'''
