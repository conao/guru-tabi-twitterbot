#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def parsePage(r):
    soup = BeautifulSoup(r.text, 'lxml')
    
def fetchPage():
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)
    return r

def main():
    """
    entry point for guru_tabi
    """

    r = fetchPage()
    parsePage(r)
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
