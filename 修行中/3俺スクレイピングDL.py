# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 21:51:59 2020

@author: YAMADA HIDEYUKI
"""
# 手動で俺が写真のurlを入れてやってみる
# 元のサイトhttp://www.dousyoko.net/blog-entry-2624.html
# タイトル 【SAO】ボス攻略前にアスナと中出しセックス！【エロ漫画同人誌】  同人エロ漫画書庫 同書庫(ドウショコ)
import requests
import os

url_image = 'http://file.dousyoko.net/uploads/old/001_thumb_20140601223626.jpg'

r_image = requests.get(url_image)
if r_image.status_code == 200:
    print(r_image.headers['Content-Type'])

    filename_image = os.path.basename(url_image)
    # いずれの場合もos.path.basename()でURLからファイル名を抽出してその名前で保存している。
    print(filename_image)
    print(type(filename_image))

    with open(os.path.join('./image/' + filename_image), 'wb') as f:
        f.write(r_image.content)