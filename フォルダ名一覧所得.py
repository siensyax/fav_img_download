# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:19:01 2020

@author: YAMADA HIDEYUKI
"""

import os

path = './fav_img'  #ディレクトリ一覧を取得したいディレクトリ
files = []

for x in os.listdir(path):
    if os.path.isdir(path + '/' + x):  #パスに取り出したオブジェクトを足してフルパスに
        os.listdir(path + '/' + x)

print(files)
