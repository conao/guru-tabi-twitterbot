#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def fetchPage():
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)

def main():
    """
    entry point for guru_tabi
    """
    fetchPage()
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
