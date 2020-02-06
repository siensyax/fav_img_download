# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 03:26:53 2020

@author: YAMADA HIDEYUKI

元サイト：https://qiita.com/ozaki_physics/items/c17ca626b480d352e90f
f12で開いた時の開発者ツールで
imgタグのsrcsetプロパティをurlとして指定したらどうなるか試した
"""


import requests

url = "https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F212705%2F3e18fdfd-4bf9-4549-1363-b2ceff7fba59.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=052a89599d2c4a8c9aed7e3663849dcb 1x"
file_name = "Qiitaの画像4.jpg"

response = requests.get(url)
image = response.content

with open(file_name, "wb") as img:
    img.write(image)
