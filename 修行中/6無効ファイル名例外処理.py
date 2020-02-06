# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 06:05:34 2020

@author: YAMADA HIDEYUKI
"""

import os


strings = ['http://file.dousyoko.net/uploads/setting/dousyokobanner.png',
'http://file.dousyoko.net/uploads/old/000_e_20140601223619.jpg',
'http://file.dousyoko.net/uploads/old/001_thumb_20140601223626.jpg',
'http://file.dousyoko.net/uploads/old/002_thumb_20140601223631.jpg',
'http://file.dousyoko.net/uploads/old/003_thumb_20140601223635.jpg',
'http://file.dousyoko.net/uploads/old/004_thumb_20140601223640.jpg',
'http://file.dousyoko.net/uploads/old/005_thumb_20140601223644.jpg',
'http://file.dousyoko.net/uploads/old/006_thumb_20140601223649.jpg',
'http://file.dousyoko.net/uploads/old/007_thumb_20140601223654.jpg',
'http://file.dousyoko.net/uploads/old/008_thumb_20140601223659.jpg',
'http://file.dousyoko.net/uploads/old/009_thumb_20140601223703.jpg',
'http://file.dousyoko.net/uploads/old/010_thumb_20140601223709.jpg',
'http://file.dousyoko.net/uploads/old/011_thumb_20140601223714.jpg',
'http://file.dousyoko.net/uploads/old/012_thumb_20140601223719.jpg',
'http://file.dousyoko.net/uploads/old/013_thumb_20140601223723.jpg',
'http://file.dousyoko.net/uploads/old/014_thumb_20140601223727.jpg',
'http://file.dousyoko.net/uploads/old/015_thumb_20140601223732.jpg',
'http://file.dousyoko.net/uploads/old/016_thumb_20140601223735.jpg',
'https://rranking13.ziyu.net/rranking.gif',
'https://pranking10.ziyu.net/img.php?dousyoko1']

esc_str = r'\/:*?"<>|'
print(len(strings))
for string in strings:
    fname = os.path.basename(string)
    # print(fname)
    if r'/' in fname or r':' in fname or r'*' in fname or r'?' in fname or r'"' in fname or r'<' in fname or r'>' in fname or r'|' in fname:
        pass
    else:
        print(fname)

# 上のifとelse文の組み合わせで一応ファイル名として使えない文字を抜いたものだけを表示できる
# ぶっちゃけあり得るのが?くらいしか考えにくいからそれを回避するだけでもいいかもしれないなあ
