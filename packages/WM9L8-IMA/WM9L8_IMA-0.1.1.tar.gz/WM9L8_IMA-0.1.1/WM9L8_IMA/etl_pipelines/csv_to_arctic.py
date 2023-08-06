import os
import pandas as pd
from typing import List, Dict
from arcticdb import Arctic
from logging import getLogger
import click

CSV_PATH = '../data/'
DB_PATH = 'lmdb:////mnt/c/Users/sharl/repos/DTS/BigData/WM9L8-IMA/astore'
S3_PATH = "s3://s3.eu-west-2.amazonaws.com:manstocks?region=eu-west-2&access=AKIAVHAD6ZB4RYHDPBWA&secret=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

class ArcticInitializer:
    def __init__(self, dbpath:str, libname:str):
        self.dbpath = dbpath
        self.libname = libname

    def get_db(self):
        return Arctic(self.dbpath)
    
    def create_library(self):
        ac = self.get_db()
        if self.libname not in ac.list_libraries():
            ac.create_library(self.libname)
    
    def get_library(self):
        return self.get_db()[self.libname]

def extract_csv(csv_path: List) -> Dict:
    csv_list = os.listdir(csv_path)
    csv_hash = {}
    for csv in csv_list:
        stock = csv.split('.csv')[0]
        csv_hash[stock] = pd.read_csv(f'../data/{csv}')
    return csv_hash

@click.command()
@click.option('--library', prompt='Enter library name', default='test')
@click.option('--csv-path', prompt='Enter path for csv files', default='../data/')
def csv_to_arctic(library, csv_path):
    data = extract_csv(csv_path)
    arctic = ArcticInitializer(S3_PATH, library)
    arctic.create_library()
    lib = arctic.get_library()

    for stock in data:
        lib.write(stock, data[stock])

if __name__=='__main__':
    csv_to_arctic()




