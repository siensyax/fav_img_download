# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 03:36:34 2020

@author: YAMADA HIDEYUKI
一応サイトとかを参考にしてtimeoutのerrorをexceptで受けているが
実際のコードでは使わない．そこまでしてもあんまり変わらん
"""

import requests
from bs4 import BeautifulSoup
import os
from time import sleep
# 証明書エラーの表示を消す
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

url = 'http://www.dousyoko.net/blog-entry-2624.html'

# https://blog.cosnomi.com/posts/1259/
# タイムアウトは明示的に指定しないとずっとループするらしい
from requests.exceptions import Timeout
try:
    r = requests.get(url, verify = False, timeout = (10.0, 30.0))
    # SSLErrorとか出て，証明書を確認できません的なエラー出てくる
    # で，chrome上でも同じようなことが起きる．
    # サイトがhttpなため
    # https://qiita.com/sta/items/6d08151fd9b20fa8b319
    # 無理やり解決
    # getメソッドのverify = Falseの部分

    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    # 出てたエラーをgoogle翻訳させたところタイムアウトエラーだったので
    # 公式ドキュメントでtimeoutの秒数の指定法っぽいのを見つけて
    # timeout時間を長めに設定した．floatで指定する必要あり
    if r.status_code == 200:
        # print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.find_all('img')
        print(len(imgs))
        title = soup.title.text
        if not os.path.exists('./' + title):
            os.mkdir('./' + title)
        for img in imgs:
            sleep(3)  # 紳士協定の3秒ルール
            # 絶対に俺のほしい漫画の写真がないはずのwordpresのスタイルの部分を抜く
            if not 'wordpress' in img['src']:
                img_src = img['src']
                # print(img_src)
                # img_srcはurlの形になっている．
                r_image = requests.get(img_src, verify = False, timeout = (30.0, 300.0))
                # いずれの場合もos.path.basename()でURLからファイル名を抽出
                filename_image = os.path.basename(img_src)
                print(filename_image)
                if r_image.status_code == 200:
                    with open(os.path.join('./' + title + '/' + filename_image), 'wb') as f:
                        f.write(r_image.content)

except Timeout:
  # エラーページを表示させるなどの処理
  print('Time out Error')
