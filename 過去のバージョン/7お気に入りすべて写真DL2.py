# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 06:49:45 2020

@author: YAMADA HIDEYUKI

とりま何とか動くようになったはずなので
空き容量のまだ割と余っているDドライブで実行する

写真のファイルサイズが明らかに小さい場合は，
保存が途中まで？しかできていないのでは？と考えて
いろいろ調べて大きめのファイルをダウンロードするときは
requests.getの引数でstream = True
に指定して少しずつダウンロードするようにすればいい的なこと書いてあるけど
それだとサポートされてない形式ですはなくなった
だけどたまに中と半端にしかダウンロードができていないのが残るのは同じだった
それと多分だけど分割する分めちゃくちゃ時間かかる
し，himebookはこっちが連続アクセスしていられる時間を決めているらしくて
あんまりちんたらダウンロードしていると強制的にホストから切断される
だから元のやり方に戻す
"""

import requests
from bs4 import BeautifulSoup
import os
from time import sleep
# 証明書エラーの表示を消す
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# 写真の中にはうまくだダウンロードできないのがあったのでそれを受ける例外処理用
import requests.exceptions as ex

filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

soup_fav = BeautifulSoup(html, 'lxml')
a_tags = soup_fav.findAll("a")
for a_tag in a_tags:
    url = a_tag.get("href")
    print(url)
    try :
        r = requests.get(url, verify = False, timeout = (10.0, 30.0))
        # getメソッドのverify = Falseの部分で証明書エラー回避
        # timeout = (10.0, 30.0)の部分で時間を長めに設定した．floatで指定する必要あり
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.content, 'lxml')  # bs4にはもともとbyteからencoding推定機能あり
            # 参考サイト：https://kanji.hatenablog.jp/entry/python-requests-beautifulsoup-encoding
            imgs = soup.find_all('img')
            if not imgs == []:  # imgタグが一つでもあるサイトのみを対象にダウンロード準備
                try :  # titleタグがないサイトの回避
                    # titleを所得して写真群の保存フォルダ名とする
                    title = soup.title.text.replace('|','').replace('/','').replace(':', '').replace('?', '')
                    print(title)  # 確認用に一応コンソールにtitle名を表示
                    if not os.path.exists('./fav_img/' + title):
                        os.mkdir('./fav_img/' + title)
                        for img in imgs:  # 毎回ダウンロードしないようにmkdirと同じインデントに
                            # 絶対に俺のほしい漫画の写真がないはずのwordpresのスタイルの部分を抜く
                            if img.get('src').endswith(".jpg"):  # img_srcはurlの形になっている．
                                try:  # ここでInvalidSchemaが出る写真を載せてるサイトもあったので例外処理で受ける
                                    sleep(1)  # 紳士協定の1秒ルール
                                    img_src = img.get('src')
                                    img_name = os.path.basename(img_src)  # os.path.basename()でURLからファイル名を抽出
                                    # https://gammasoft.jp/support/solutions-of-requests-get-failed/
                                    with requests.get(img_src, verify = False, timeout = (30.0, 300.0), stream=True) as r_image :
                                    # getメソッドのverify = Falseの部分で証明書エラー回避
                                    # timeout = (30.0, 300.0)の部分で時間を長めに設定した．floatで指定する必要あり
                                    # streamを指定して少しずつダウンロードするようにする
                                    # stram=Trueの時はrequest.getにもwith文を使うべきらしい
                                    # https://qiita.com/pollenjp/items/0c39c35120cd60575647
                                        # ファイル名としてエラーになる奴や明らかに漫画でない名前の写真をはじく
                                        if r'/' in img_name or r':' in img_name or r'*' in img_name or r'?' in img_name or r'|' in img_name or 'logo' in img_name or 'baner' in img_name or 'page' in img_name or 'rank' in img_name or 'star' in img_name :
                                            pass
                                        else:
                                            if r_image.status_code == requests.codes.ok:
                                                print(img_name)
                                                img_full_path = os.path.join('./fav_img/' + title + '/' + img_name)
                                                with open(img_full_path, 'wb') as f:
                                                    f.write(r_image.content)
                                except ex.InvalidSchema:
                                    pass
                                except ex.ConnectionError:
                                    pass
                                except ex.MissingSchema:
                                    pass
                                except ex.ChunkedEncodingError:
                                    pass
                except AttributeError:  # titleタグがないサイトの回避
                    pass
    except ex.ConnectionError:
        pass
    except ex.ReadTimeout:
        pass

