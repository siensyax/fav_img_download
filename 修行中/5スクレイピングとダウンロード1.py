# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 03:36:34 2020

@author: YAMADA HIDEYUKI
"""

import requests
from bs4 import BeautifulSoup
import os
from time import sleep

url = 'http://hime-book.net/92607'

r = requests.get(url, verify = False)
# print(r.status_code)
if r.status_code == 200:
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img')
    print(len(imgs))
    title = soup.title.text
    if not os.path.exists('./' + title):
        os.mkdir('./' + title)
    for img in imgs:
        sleep(3)
        img_src = img['src']
        # print(img_src)
        # img_srcはurlの形になっている．
        r_image = requests.get(img_src)
        # いずれの場合もos.path.basename()でURLからファイル名を抽出
        filename_image = os.path.basename(img_src)
        print(filename_image)
        if r_image.status_code == 200:
            print(r_image.headers['Content-Type'])
            with open(os.path.join('./' + title + '/' + filename_image), 'wb') as f:
                f.write(r_image.content)
