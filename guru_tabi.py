#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def browsePage():
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')
    panels = soup.find_all("li", attrs = {"class": "col-4"})
    for panel in panels:
        print(panel.find("a").get("href"))
        
def main():
    """
    entry point for guru_tabi
    """

    browsePage()
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
