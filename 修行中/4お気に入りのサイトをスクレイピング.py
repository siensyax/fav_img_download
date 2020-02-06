# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 23:08:34 2020

@author: YAMADA HIDEYUKI
http://www.dousyoko.net/blog-entry-2624.html
"""

import requests
from bs4 import BeautifulSoup

url = 'http://www.dousyoko.net/blog-entry-2624.html'

r = requests.get(url, verify = False)
# print(r.status_code)
if r.status_code == 200:
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img')
    print(len(imgs))
    # のちの保存フォルダ名とするためにtitleタグを入手する
    title = soup.title
    print(title.text)
    # OKこの上の2行でちゃんとtitleタグを抽出できる．
    for img in imgs:
        # 絶対に俺のほしい漫画の写真がないはずのwordpresのスタイルの部分を抜く
        if not 'wordpress' in img['src']:
            # 多分，俺のほしい漫画の写真の形式としては保存しない形式であるgifを抜く
            img_src = img['src']
            print(img_src)
            # img_srcの中にちゃんとほしい写真のurlが含まれている．
