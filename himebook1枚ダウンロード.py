# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:28:26 2020

@author: YAMADA HIDEYUKI

himebookをダウンロードしようとすると
一枚の写真のダウンロードが長いのに
サイト側に接続できる限界時間が設定されている
超えると強制的に切断される
"""


import requests
from bs4 import BeautifulSoup
import os
from time import sleep

# 証明書エラーの表示を消す
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# リトライ設定用
from urllib3.util import Retry
from requests.adapters import HTTPAdapter


image_url = 'http://img.himebook.net/pickup/big/414.jpg'

# リトライを記述部分
session = requests.Session()
retries = Retry(total=5,  # リトライ回数
                backoff_factor=2,  # sleep時間
                status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount('http://', HTTPAdapter(max_retries=retries))

r_imgage = requests.get(image_url, verify = False, timeout = (10.0, 30.0))

img_name = os.path.basename(image_url)  # os.path.basename()でURLからファイル名を抽出

if r_image.status_code == 200:
    print(img_name)
    with open(img_full_path, 'wb') as f:
        f.write(r_image.content)
