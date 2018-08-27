#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pdb
import os
import twitter

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
    if not linedata[2].startswith("http"):
        linedata[2] = "https:" + linedata[2]
    if not linedata[3].startswith("http"):
        linedata[3] = "https:" + linedata[3]
    
    consumer_key = "UtVxSquH0tf0iKQpvOha7nFzg"
    consumer_secret = "eI2pQUz2t2bVkFwOQg04ztw81Xyf5BNjRtNlt26uMWqBZWDU36"
    
    twitter_creds = os.path.expanduser("~/.secret/guru_tabi_twitter")
    if not os.path.exists(twitter_creds):
        twitter.oauth_dance("guru_tabi", consumer_key, consumer_secret, twitter_creds)

    oauth_token, oauth_secret = twitter.read_token_file(twitter_creds)
    
    t_auth = twitter.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
    t = twitter.Twitter(auth = t_auth)
    

    text = "%s %s" % (linedata[1], linedata[2])
    img_url = linedata[3]
    r = requests.get(img_url)
    imgdata = r.content

    img_upload = twitter.Twitter(domain='upload.twitter.com', auth = t_auth)
    id_img = img_upload.media.upload(media = imgdata)["media_id_string"]
    t.statuses.update(status = text, media_ids = ",".join([id_img]))
    
    with open("img/%s.jpg" % linedata[0], "wb") as fout:
        fout.write(imgdata)
        
    # t.statuses.update(status=text)

    print(linedata[0])
    
def main():
    """
    entry point for guru_tabi
    """

    dt = np.dtype([('inx', np.int),
                   ('name', np.unicode_, 256),
                   ('url', np.unicode_, 512),
                   ('img_url', np.unicode_, 512)])
    data = browsePage(dt)
    writeData(data, dt)
    
if __name__ == '__main__':
    print("guru_tabi v0.1")

main()
