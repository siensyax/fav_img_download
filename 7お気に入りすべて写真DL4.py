# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 06:49:45 2020

@author: YAMADA HIDEYUKI

PILのImageを使って保存した画像がちゃんと画像であるかを判定して
画像としてうまくダウンロードできていなかったら画像の保存をやり直させるようにする

titleが長すぎるときに，テキトーに短くするようにする．
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
            # 関数化して戻り値を指定してやる関係上，2回画像名を表示しないように戻り値化
            # print(img_name)  # 保存する画像の名前を表示してちゃんとできそうか確かめる
            img_full_path = os.path.join('./fav_img/' + url_domain + '/' + title + '/' + img_name)
            with open(img_full_path, 'wb') as f:  # 画像はバイナリ形式で書き込まないとあかん
                f.write(r_image.content)  # 画像を書き込んでローカルに保存する
                sleep(1)  # 紳士協定の1秒ルール
                return img_name, img_full_path  # if分でちゃんと実行された方出ないと画像がないのでfull_pathも存在しなくなってエラーになる


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
                    if len(title) >= 50 :
                        #windowsの仕様でフォルダ名の末尾になるスペースと.は自動で消されてしまい後の画像を保存する際のパスが存在しなくなる
                        # https://ja.stackoverflow.com/questions/47292/windows%E3%81%A7%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%90%8D%E3%81%AE%E6%9C%AB%E5%B0%BE%E3%83%89%E3%83%83%E3%83%88%E3%81%8C%E7%84%A1%E8%A6%96%E3%81%95%E3%82%8C%E3%82%8B%E6%8C%99%E5%8B%95%E3%81%AE%E7%94%B1%E6%9D%A5
                        title = title[:50].strip().strip(".")  # strip 先頭と末尾のスペースや.を削除してくれるメソッド
                        # https://uxmilk.jp/12804
                        print(title)
                    if not os.path.exists('./fav_img/' + url_domain + '/' + title):
                        os.makedirs('./fav_img/' + url_domain + '/' + title)
                        for img in imgs:  # 毎回ダウンロードしないようにmkdirと同じインデントに
                            if img.get('src').endswith(".jpg"):  # img_srcはurlの形になっていて，末尾がjpgのものだけに処理をする．
                                try:  # ここでInvalidSchemaが出る写真を載せてるサイトもあったので例外処理で受ける
                                    image_save(img)  # 画像を保存する処理をimgを引数として実行する
                                    # 処理の戻り値として指定したimg_nameとimg_full_pathをこちらでも使えるように同じ変数名へ代入する
                                    img_name, img_full_path = image_save(img)
                                    print(img_name)
                                    try :# Imageで保存した画像を開いてみる
                                        Image.open(img_full_path.strip(), mode='r')  #問題なくできたら何もしない
                                        pass
                                    except OSError as e:  # 画像として認識されていませんよというエラーが来たら
                                        print(e)  # エラー文を表示させて
                                        image_save(img)  # もう一度画像の保存からやり直す．
                                except ex.InvalidSchema as e:
                                    print(e)
                                except ex.ConnectionError as e:
                                    print(e)
                                except ex.MissingSchema as e:
                                    print(e)
                                except ex.ChunkedEncodingError as e:
                                    print(e)
                                except TypeError as e:  # image_save関数の引数であるimgがNoneの時を除くようにするため
                                    print(e)
                except AttributeError as e:  # titleタグがないサイトの回避
                    print(e)
    except ex.ConnectionError as e:
        print(e)
    except ex.ReadTimeout as e:
        print(e)
