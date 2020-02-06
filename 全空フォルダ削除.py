# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:19:01 2020

@author: YAMADA HIDEYUKI
"""

import os

path = './fav_img'  #ディレクトリ一覧を取得したいディレクトリ

remove_count = 0  # 削除したフォルダ数を数えるための仮変数
remove_dir_name_list = []

for x in os.listdir(path):
    if os.path.isdir(path + '/' + x):  #パスに取り出したオブジェクトを足してフルパスに
        child_f = os.listdir(path + '/' + x)
        # print(child_f == None)
        if child_f == []:
            os.rmdir(path + '/' + x)
            remove_dir_name_list.append(x)
            remove_count = remove_count + 1

print(str(remove_count) + '個の空フォルダを削除しました')
print('削除したフォルダ名は')
print(remove_dir_name_list)
