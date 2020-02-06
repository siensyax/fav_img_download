# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:50:35 2020

@author: YAMADA HIDEYUKI
"""

# fav_href_list.txtに保存された中でたまにurlが変なエンコーディングっぽいところもあるがもともとそういうurlだと思う

from bs4 import BeautifulSoup


filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'  # 読み込むhtmlを変数に入れとく
with open(filepath , encoding='utf-8') as f:  # withを使って少しかっこよくファイルを開いてファイルオブジェクトを生成
    html = f.read()  # ファイルオブジェクトを読み込んだ結果をhtmlという変数に代入

# htmlの解析
# aタグのhrefリンクだけを取り出す
soup_fav = BeautifulSoup(html, 'lxml')  # Beautifulsoupでhtmlをlxmlというパーサー(hmtlを解析するツール)で解析する
a_tags = soup_fav.find_all("a")  # すべてのaタグをfind_allメソッドを用いてリスト形式で所得
urls = []  # 所得したurlの一覧を格納するためのリストを先に生成しておく
for a_tag in a_tags:  # a_tagsからfor loopで一つずつ取り出して仮変数a_tagに代入する
    url = a_tag.get("href")  # a_tagの中からgetメソッドを用いてhrefプロパティのなかのValueだけ取り出してurlという変数の中へ代入する
    print(url)  # urlを表示して，ちゃんとurlを取り出せたかを確認する
    urls.append(url)  # urlの一覧を格納するurlsに追加する

print(len(urls))  # ちゃんとurlsに追加できているか確認する

# ファイルに出力する部分
# fav_href_list.txtというテキストファイルに保存する
with open('fav_href_list.txt', 'w', encoding='utf-8') as f:  # またまたwith分でテキストファイルを開いたファイルオブジェクトを生成する
    # 今回は追記型(a = append)で開く
    for url in urls:  # 上で作ったurlの一覧からforループを使って一つずつ取り出す
        print(url, file=f)  # print関数の引数にファイルオブジェクトを指定して，urlを保存する
