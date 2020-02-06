# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 00:49:06 2019

@author: YAMADA HIDEYUKI

お気に入りバーの構造
<DT><H3 LAST_MODIFIED="1538313598" >_Favorites_Bar_</H3>
"""

from bs4 import BeautifulSoup


filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

# 前にやったaタグをすべて取り出すを復習
'''
a_tags = soup.findAll("a")
for a_tag in a_tags:
    print(a_tag.string)
'''

# 次にお気に入りバーの構造からh3タグをすべて取り出す
'''
h3_tags = soup.findAll("h3")
for h3_tag in h3_tags:
    print(h3_tag.string)
'''

# その次にh3タグの中から取り出したいお気に入りバーだけを取り出す
'''
h3_tags = soup.findAll("h3")
for h3_tag in h3_tags:
    if h3_tag.string in ">_Favorites_Bar_":
        print(h3_tag.string)
'''
# サイト「エロ漫画の森」のアドレスだけを取り出す
a_tags = soup.findAll("a")
# print(a_tags[10])  # ハイパーリンク1つだけ取り出せる
# find_allの返り価は普通にリストなので
# print(a_tags[1 : 10])  # ハイパーリンクを欲しい分だけ取り出せる
# 参考サイトhttps://note.nkmk.me/python-str-search/
for a_tag in a_tags[:5]:
    hl = a_tag.get("href")
    print(hl)  # すべてのハイパーリンクを表示
    # in文は今まで思ってたのとは逆の順番の参照
    # 入ってたらTrueを返すからif文とうまく使える
    # if "eromanganomori" in hl :
      #   print(hl)
