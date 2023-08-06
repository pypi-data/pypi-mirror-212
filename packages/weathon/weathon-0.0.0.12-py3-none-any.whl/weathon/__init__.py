# -*- coding: utf-8 -*-
# @Time    : 2022/10/2 08:28
# @Author  : LiZhen
# @FileName: __init__.py.py
# @github  : https://github.com/Lizhen0628
# @Description:
__version__ = '0.0.0.12'
__author__ = 'LiZhen'
__email__ = '16621660628@163.com'


import os
from pathlib import Path

DATA_DIR = Path.home() / "data"
os.environ["DATA_DIR"] = str(DATA_DIR)



# python setup.py sdist upload
