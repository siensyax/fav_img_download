# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 00:42:52 2020

@author: YAMADA HIDEYUKI
"""

# 参考サイト：https://ai-inter1.com/python-regex/
# 全てのドメイン名を指定できる正規表現は下記のようである
# https?://[^/]+/
# [^/]の部分がドメイン名が入っている/以外の文字列という意味のため

# compile後match
# repatter = re.compile(pattern)
# result = repatter.match(content)

# urlの一覧を所得する
import requests
from bs4 import BeautifulSoup
import re


filepath = 'Microsoft_Edge_‎2019_‎12_‎28.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

url_list = []
soup_fav = BeautifulSoup(html, 'lxml')
a_tags = soup_fav.findAll("a")
for a_tag in a_tags:
    url = a_tag.get("href")
    # url_compile = re.compile(r'https?://[^/]+/')
    # url_domain = url_compile.match(url)
    url_domain2 = re.search(r'https?://[^/]+/', url)
    # print(url_domain2)
    # print(url_domain2.group())  # groupメソッドを加えると文字列だけ取り出せる
    url_list.append(url_domain2.group())

# print(url_list)
# print(len(url_list))
# listのままだと重複したドメインが残ってしまう
# set型に変換してやると重複を許さないらしい
# https://lanchesters.site/python-list-uniq/
url_sets = set(url_list)
print(url_sets)
print(len(url_sets))
# ドメイン名一覧をファイルに保存する
with open('dir_name_list.txt', 'w', encoding='utf-8') as t:
    for url_set in url_sets:
        print(url_set, file=t)
