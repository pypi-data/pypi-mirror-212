import os
import lmdb

DB_PATH = '/mnt/c/Users/sharl/repos/DTS/BigData/WM9L8-IMA/astore'
cwd = os.getcwd()
env = lmdb.open(DB_PATH, map_size=1000)