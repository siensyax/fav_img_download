# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 03:36:34 2020

@author: YAMADA HIDEYUKI
実際にお気に入りサイトのリストを突っ込む前の
画像のダウンロードをするための記述元
"""

import requests
from bs4 import BeautifulSoup
import os
from time import sleep
# 証明書エラーの表示を消す
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

url = 'http://eromanga-everyday.com/%e3%80%90%e3%82%a8%e3%83%ad%e6%bc%ab%e7%94%bb%e3%80%91%e5%b9%bc%e3%81%aa%e3%81%98%e3%81%bf%e3%81%ae%e5%b7%a8%e4%b9%b3%e7%be%8e%e5%b0%91%e5%a5%b3%e5%a5%b3%e5%ad%90%e6%a0%a1%e7%94%9f%e3%81%a8%e3%81%af/'

r = requests.get(url, verify = False, timeout = (10.0, 30.0))
# getメソッドのverify = Falseの部分で証明書エラー回避
# timeout = (10.0, 30.0)の部分で時間を長めに設定した．floatで指定する必要あり
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img')
    print(len(imgs))  # そのサイトに含まれていたimgタグの個数を表示
    title = soup.title.text.replace('|','')  # titleを所得して写真軍の保存フォルダ名とする
    if not os.path.exists('./' + title):
        os.mkdir('./' + title)
    for img in imgs:
        sleep(3)  # 紳士協定の3秒ルール
        # 絶対に俺のほしい漫画の写真がないはずのwordpresのスタイルの部分を抜く
        if not 'wordpress' in img['src']:
            img_src = img['src']  # img_srcはurlの形になっている．
            r_image = requests.get(img_src, verify = False, timeout = (30.0, 300.0))
            filename_image = os.path.basename(img_src)  # os.path.basename()でURLからファイル名を抽出
            if r'/' in filename_image or r':' in filename_image or r'*' in filename_image or r'?' in filename_image or r'"' in filename_image or r'<' in filename_image or r'>' in filename_image or r'|' in filename_image:
                pass
            else:
                if r_image.status_code == 200:
                    print(filename_image)
                    with open(os.path.join('./' + title + '/' + filename_image), 'wb') as f:
                        f.write(r_image.content)
