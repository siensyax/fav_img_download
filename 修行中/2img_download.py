# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 03:04:18 2020

@author: YAMADA HIDEYUKI

元サイト：https://qiita.com/ozaki_physics/items/c17ca626b480d352e90f
そのまんま
"""

import requests

url = "https://camo.qiitausercontent.com/42a9852fb9ad88e63f10442b835315424a13c96b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3231323730352f33653138666466642d346266392d343534392d313336332d6232636566663766626135392e706e67"
file_name = "Qiitaの画像.jpg"

response = requests.get(url)
image = response.content

with open(file_name, "wb") as img:
    img.write(image)
