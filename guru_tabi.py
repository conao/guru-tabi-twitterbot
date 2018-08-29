#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pdb
import os
import twitter
import feedgenerator

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
        str_area = panel.find("p", attrs = {"class": "panel__layer-txt"}).text
        str_author = panel.find("p", attrs = {"class": "panel__writer"}).text
        inx_match = re_inx.search(element_a.get("href"))
        # pdb.set_trace()
        data[i] = (inx_match.group("inx") if inx_match else 0,
                   str_area,
                   str_author,
                   element_img.get("alt"),
                   element_a.get("href"),
                   element_img.get("src"))
    return data

def writeData(data, dt):
    data_filename = "data.csv"
    if os.path.exists(data_filename):
        df = pd.read_csv(data_filename)
    else:
        df = pd.DataFrame(np.empty(0, dtype = dt))

    for line in data:
        if np.all(df["inx"] != line[0]):
            postTwitter(line)
        
    df = pd.concat([df, pd.DataFrame(data)])
    df = df.drop_duplicates("inx")

    df.to_csv(data_filename, index=False)

def postTwitter(linedata):
    i_inx = 0
    i_area = 1
    i_author = 2
    i_description = 3
    i_url = 4
    i_img_url = 5

    if not linedata[i_url].startswith("http"):
        linedata[i_url] = "https:" + linedata[i_url]
    if not linedata[i_img_url].startswith("http"):
        linedata[i_img_url] = "https:" + linedata[i_img_url]
    
    consumer_key = "UtVxSquH0tf0iKQpvOha7nFzg"
    consumer_secret = "eI2pQUz2t2bVkFwOQg04ztw81Xyf5BNjRtNlt26uMWqBZWDU36"
    
    twitter_creds = os.path.expanduser("~/.secret/guru_tabi_twitter")
    if not os.path.exists(twitter_creds):
        twitter.oauth_dance("guru_tabi", consumer_key, consumer_secret, twitter_creds)

    oauth_token, oauth_secret = twitter.read_token_file(twitter_creds)
    
    t_auth = twitter.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
    t = twitter.Twitter(auth = t_auth)
    

    text = "%s(%s) - %s %s" % (linedata[i_description], linedata[i_author], linedata[i_area], linedata[i_url])
    img_url = linedata[i_img_url]
    r = requests.get(img_url)
    imgdata = r.content

    img_upload = twitter.Twitter(domain='upload.twitter.com', auth = t_auth)
    id_img = img_upload.media.upload(media = imgdata)["media_id_string"]
    t.statuses.update(status = text, media_ids = ",".join([id_img]))
    
    with open("img/%s.jpg" % linedata[i_inx], "wb") as fout:
        fout.write(imgdata)
        
    # t.statuses.update(status=text)

    print(linedata[i_inx])
    
def main():
    """
    entry point for guru_tabi
    """

    dt = np.dtype([('inx', np.int),
                   ('area', np.unicode_, 256),
                   ('author', np.unicode_, 32),
                   ('name', np.unicode_, 256),
                   ('url', np.unicode_, 512),
                   ('img_url', np.unicode_, 512)])
    data = browsePage(dt)
    writeData(data, dt)
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
