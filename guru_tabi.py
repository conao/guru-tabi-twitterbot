#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pdb

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def browsePage():
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')
    panels = soup.find_all("li", attrs = {"class": "col-4"})

    re_inx = re.compile(r"/a_(?P<inx>[0]*)/")
    dt = np.dtype([('inx', np.int), ('url', np.unicode_, 512), ('name', np.unicode_, 256)])
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
        
def main():
    """
    entry point for guru_tabi
    """

    data = browsePage()
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
