# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:14:32 2020

@author: YAMADA HIDEYUKI
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


url = 'http://hime-book.net/92607'

# リトライを記述部分
session = requests.Session()
retries = Retry(total=5,  # リトライ回数
                backoff_factor=2,  # sleep時間
                status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount('http://', HTTPAdapter(max_retries=retries))

r = requests.get(url, verify = False, timeout = (10.0, 30.0))
# getメソッドのverify = Falseの部分で証明書エラー回避
# timeout = (10.0, 30.0)の部分で時間を長めに設定した．floatで指定する必要あり

if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'lxml')  # bs4にはもともとbyteからencoding推定機能あり
    # 参考サイト：https://kanji.hatenablog.jp/entry/python-requests-beautifulsoup-encoding
    imgs = soup.find_all('img')
    if not imgs == []:  # imgタグが一つでもあるサイトのみを対象にダウンロード準備
        try :  # titleタグがないサイトの回避
            title = soup.title.text.replace('|','').replace('/','').replace(':', '').replace('?', '')
            print(title)  # 確認用に一応コンソールにtitle名を表示
            if not os.path.exists('./' + title):
                os.mkdir('./' + title)
            for img in imgs:  # 毎回ダウンロードしないようにmkdirと同じインデントに
                if img.get('src').endswith(".jpg"):  # img_srcはurlの形になっている．末尾がjpgのものだけにする
                    sleep(1)  # 紳士協定の1秒ルール
                    img_src = img.get('src')
                    img_name = os.path.basename(img_src)  # os.path.basename()でURLからファイル名を抽出
                    # https://gammasoft.jp/support/solutions-of-requests-get-failed/
                    # リトライを記述部分
                    session = requests.Session()
                    retries = Retry(total=3,  # リトライ回数
                                    backoff_factor=1,  # sleep時間
                                    status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
                    session.mount("https://", HTTPAdapter(max_retries=retries))
                    session.mount('http://', HTTPAdapter(max_retries=retries))
                    # https://qiita.com/azumagoro/items/3402facf0bcfecea0f06
                    r_image = requests.get(img_src, verify = False, timeout = (5.0, 30.0), stream=False)
                    # getメソッドのverify = Falseの部分で証明書エラー回避
                    # timeout = (5.0, 90.0)の部分で時間を長めに設定した．floatで指定する必要あり
                    r_image.raw.decode_content = True  # ここを指定すれば空のファイルが返ってくるのを回避できる
                    # https://www.dev2qa.com/how-to-download-image-file-from-url-use-python-requests-or-wget-module/
                    # ファイル名としてエラーになる奴や明らかに漫画でない名前の写真をはじく
                    if r'/' in img_name or r':' in img_name or r'*' in img_name or r'?' in img_name or r'|' in img_name or 'logo' in img_name or 'baner' in img_name or 'page' in img_name or 'rank' in img_name or 'star' in img_name or 'wordpress' in img_name:
                        pass
                    else:
                        if r_image.status_code == 200:
                            print(img_name)
                            img_full_path = os.path.join('./fav_img/' + title + '/' + img_name)
                            with open(img_full_path, 'wb') as f:
                                f.write(r_image.content)
        except AttributeError as e:  # titleタグがないサイトの回避
                    print(e)
