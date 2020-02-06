# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:30:39 2020

@author: YAMADA HIDEYUKI
"""

import glob
import os

for folder in glob.glob('fav_img/**/', recursive=True):
    print(os.path.basename(folder.rstrip(os.sep)))
