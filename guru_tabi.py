#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

"""
guru_tabi is twitter-bot for guru-tabi(https://gurutabi.gnavi.co.jp/a/).
"""

def main():
    """
    entry point for guru_tabi
    """
    target_url = '***'
    r = requests.get(target_url)
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
