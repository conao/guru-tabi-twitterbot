#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pdb
import os

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def browsePage(dt):
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')
    panels = soup.find_all("li", attrs = {"class": "col-4"})

    re_inx = re.compile(r"/a_(?P<inx>[0-9]*)/")    
    data = np.empty(len(panels), dtype = dt)
    
    for (i, panel) in enumerate(panels):
        element_a = panel.find("a")
        element_img = panel.find("img")
        inx_match = re_inx.search(element_a.get("href"))
        # pdb.set_trace()
        data[i] = (inx_match.group("inx") if inx_match else 0,
                   element_img.get("src"),
                   element_img.get("alt"))
    return data

def writeData(data, dt):
    data_filename = "data.csv"
    if os.path.exists(data_filename):
        df = pd.read_csv(data_filename)
    else:
        df = pd.DataFrame(np.empty(0, dtype = dt))
        
    df = pd.concat([df, pd.DataFrame(data)])
    df.drop_duplicates("inx")

    df.to_csv(data_filename)
    
def main():
    """
    entry point for guru_tabi
    """

    dt = np.dtype([('inx', np.int), ('url', np.unicode_, 512), ('name', np.unicode_, 256)])
    data = browsePage(dt)
    writeData(data, dt)
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
