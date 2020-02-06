# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 05:04:19 2020

@author: YAMADA HIDEYUKI
"""

import re
import os


# テキストファイル読み込み部
filepath = 'fav_href_list.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.readlines()  # テキストファイルを読全てを1行ずつみ込んでリスト形式で格納

# テキストファイルの読み込み結果をforループで1つずつ取り出してドメイン名だけ取り出す処理
for url in text:
    url_domain2 = re.search(r'https?://[^/]+/', url)  # 正規表現でドメイン名のある部分周辺だけを取り出す
    if 'https' in url_domain2.group():
        url_domain = url_domain2.group()[8:-2]  # groupメソッドで値だけを取り出して，文字列の位置を指定して，httpとかの余計な部分をなくす
    else:
        url_domain = url_domain2.group()[7:-2]  # groupメソッドで値だけを取り出して，文字列の位置を指定して，httpとかの余計な部分をなくす

    # ドメイン名のテキストファイルでドメインごとに分けてurlを保存する
    t_path = os.path.join('./domain/' + url_domain + '.txt')
    with open(t_path, 'a', encoding='utf-8') as t:
        print(url[:-2], file=t)  # urlに改行文字が含まれているのでそれは[:-2]の部分で取り除いている
