# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 21:17:42 2020

@author: YAMADA HIDEYUKI
"""

'''
https://note.nkmk.me/python-requests-usage/
画像やzipファイルなどをダウンロード
画像やzipファイルなどのテキストではないデータをダウンロードすることも可能。

Responseのcontent属性で取得できるバイナリデータをそのままバイナリとして保存するだけ。

画像の例。
'''

import requests
import os

url_image = 'https://www.python.org/static/community_logos/python-logo.png'

r_image = requests.get(url_image)

print(r_image.headers['Content-Type'])
# image/png

filename_image = os.path.basename(url_image)
# いずれの場合もos.path.basename()でURLからファイル名を抽出してその名前で保存している。
print(filename_image)
# python-logo.png


# imageフォルダを勝手に作ってはくれない
# だけどちゃんと作ってやれば保存される．
with open(os.path.join('./image/' + filename_image), 'wb') as f:
    f.write(r_image.content)
