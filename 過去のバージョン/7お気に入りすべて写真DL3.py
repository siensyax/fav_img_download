# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 06:49:45 2020

@author: YAMADA HIDEYUKI

後で写真を整理しやすいようにドメイン名でフォルダを分けながら写真を保存するようにする

なんか接続がブロックされるようになった
himebookとosamu

今までダウンロードした画像のうち一部はサポートされてない形式と出てきたときは
今は接続できません的なhtmlが帰ってきてる
streamとかの問題じゃないかも
htmlのtitleはASUS Wireless Router RT-AC67U - Blocking Page
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

# 写真の中にはうまくだダウンロードできないのがあったのでそれを受ける例外処理用
import requests.exceptions as ex

import re  # 正規表現を使ってドメイン名だけを取り出すため

from PIL import Image  # Imageクラス？のopenメソッドを使って

filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

def image_save(img):
    img_src = img.get('src')  # imgタグからsrcプロパティの値であるURLを所得して，ダウンロードの準備する
    img_name = os.path.basename(img_src)  # os.path.basename()でURLからファイル名を抽出

    # リトライを記述部分
    session = requests.Session()
    retries = Retry(total=3,  # リトライ回数
                    backoff_factor=2,  # sleep時間
                    status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    # https://qiita.com/azumagoro/items/3402facf0bcfecea0f06

    # サイトへ情報を取りに行く処理．いろいろ引数を指定して，うまくいきやすいようにした
    r_image = requests.get(img_src, verify = False, timeout = (15.0, 90.0), stream=False)
    r_image.raw.decode_content = True  # ここを指定すれば空のファイルが返ってくるのを回避できる

    # ファイル名としてエラーになる奴や明らかに漫画でない名前の写真をはじく
    if r'/' in img_name or r':' in img_name or r'*' in img_name or r'?' in img_name or r'|' in img_name or 'logo' in img_name or 'baner' in img_name or 'page' in img_name or 'rank' in img_name or 'star' in img_name or 'wordpress' in img_name:
        pass  # 何もせずにforループへ戻る
    else:  # はじかれなかった画像だけを保存する．
        if r_image.status_code == 200:  # ちゃんと通信できた時だけ画像保存処理を行う
            print(img_name)  # 保存する画像の名前を表示してちゃんとできそうか確かめる
            img_full_path = os.path.join('./fav_img/' + url_domain + '/' + title + '/' + img_name)
            with open(img_full_path, 'wb') as f:  # 画像はバイナリ形式で書き込まないとあかん
                f.write(r_image.content)  # 画像を書き込んでローカルに保存する
                sleep(1)  # 紳士協定の1秒ルール


soup_fav = BeautifulSoup(html, 'lxml')
a_tags = soup_fav.findAll("a")
for a_tag in a_tags:
    url = a_tag.get("href")
    print(url)

    # 正規表現を使ってドメイン名だけを取り出す処理部分
    url_domain2 = re.search(r'https?://[^/]+/', url)  # 正規表現でドメイン名のある部分周辺だけを取り出す
    if 'https' in url_domain2.group():
        url_domain = url_domain2.group()[8:-1]  # groupメソッドで値だけを取り出して，文字列の位置を指定して，httpとかの余計な部分をなくす
    else:
        url_domain = url_domain2.group()[7:-1]  # groupメソッドで値だけを取り出して，文字列の位置を指定して，httpとかの余計な部分をなくす
    # print(url_domain)

    try :  # 実際にネットに接続して情報を取ってくる部分
        # リトライを記述部分
        session = requests.Session()
        retries = Retry(total=5,  # リトライ回数
                        backoff_factor=2,  # sleep時間
                        status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
        session.mount("https://", HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))
        # https://qiita.com/azumagoro/items/3402facf0bcfecea0f06
        r = requests.get(url, verify = False, timeout = (10.0, 30.0))
        # getメソッドのverify = Falseの部分で証明書エラー回避
        # timeout = (10.0, 30.0)の部分で時間を長めに設定した．floatで指定する必要あり
        sleep(1)  # 紳士協定の1秒ルール
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')  # bs4にはもともとbyteからencoding推定機能あり
            # 参考サイト：https://kanji.hatenablog.jp/entry/python-requests-beautifulsoup-encoding
            imgs = soup.find_all('img')
            if not imgs == []:  # imgタグが一つでもあるサイトのみを対象にダウンロード準備
                try :  # titleタグがないサイトの回避
                    # titleを所得して写真群の保存フォルダ名とする
                    title = soup.title.text.replace('|','').replace('/','').replace(':', '').replace('?', '')
                    print(title)  # 確認用に一応コンソールにtitle名を表示
                    if not os.path.exists('./fav_img/' + url_domain + '/' + title):
                        os.makedirs('./fav_img/' + url_domain + '/' + title)
                        # https://note.nkmk.me/python-os-mkdir-makedirs/
                        for img in imgs:  # 毎回ダウンロードしないようにmkdirと同じインデントに
                            if img.get('src').endswith(".jpg"):  # img_srcはurlの形になっている．
                                print(img)
                                try:  # ここでInvalidSchemaが出る写真を載せてるサイトもあったので例外処理で受ける
                                    image_save(img)
                                except ex.InvalidSchema as e:
                                    print(e)
                                except ex.ConnectionError as e:
                                    print(e)
                                except ex.MissingSchema as e:
                                    print(e)
                                except ex.ChunkedEncodingError as e:
                                    print(e)
                except AttributeError as e:  # titleタグがないサイトの回避
                    print(e)
    except ex.ConnectionError as e:
        print(e)
    except ex.ReadTimeout as e:
        print(e)
