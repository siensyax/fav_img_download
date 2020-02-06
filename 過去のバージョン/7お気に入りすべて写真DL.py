# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 06:49:45 2020

@author: YAMADA HIDEYUKI

とりま何とか動くようになったはずなので
空き容量のまだ割と余っているDドライブで実行する
"""

import requests
from bs4 import BeautifulSoup
import os
from time import sleep
# 証明書エラーの表示を消す
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

soup_fav = BeautifulSoup(html, 'lxml')
a_tags = soup_fav.findAll("a")
for a_tag in a_tags:
    url = a_tag.get("href")
    print(url)
    r = requests.get(url, verify = False, timeout = (10.0, 30.0))
    # getメソッドのverify = Falseの部分で証明書エラー回避
    # timeout = (10.0, 30.0)の部分で時間を長めに設定した．floatで指定する必要あり
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.find_all('img')
        print(len(imgs))  # そのサイトに含まれていたimgタグの個数を表示
        title = soup.title.text.replace('|','')  # titleを所得して写真軍の保存フォルダ名とする
        if not os.path.exists('./fav_img/' + title):
            os.mkdir('./fav_img/' + title)
        for img in imgs:
            sleep(3)  # 紳士協定の3秒ルール
            # 絶対に俺のほしい漫画の写真がないはずのwordpresのスタイルの部分を抜く
            if not 'wordpress' in img['src']:
                img_src = img['src']  # img_srcはurlの形になっている．
                r_image = requests.get(img_src, verify = False, timeout = (30.0, 300.0))
                img_name = os.path.basename(img_src)  # os.path.basename()でURLからファイル名を抽出
                if r'/' in img_name or r':' in img_name or r'*' in img_name or r'?' in img_name or r'|' in img_name :
                    pass
                else:
                    if r_image.status_code == 200:
                        print(img_name)
                        with open(os.path.join('./fav_img/' + title + '/' + img_name), 'wb') as f:
                            f.write(r_image.content)
