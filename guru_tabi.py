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

####################
####
####  small funcs

def addHttpScheme(target, ishttp = False):
    scheme = 'http:' if ishttp else 'https:'
    result = target
    
    if not target.startswith(scheme):
        result = scheme + target

    return result


####################
####
####  main funcs

def browsePage(dt):
    target_url = 'https://gurutabi.gnavi.co.jp/a/'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')
    panels = soup.find_all('li', attrs = {'class': 'col-4'})

    re_inx = re.compile(r'/a_(?P<inx>[0-9]*)/')    
    data = np.empty(len(panels), dtype = dt)
    
    for (i, panel) in enumerate(panels):
        element_a = panel.find('a')
        element_img = panel.find('img')
        str_area = panel.find('p', attrs = {'class': 'panel__layer-txt'}).text
        str_author = panel.find('p', attrs = {'class': 'panel__writer'}).text
        inx_match = re_inx.search(element_a.get('href'))
        # pdb.set_trace()
        data[i] = (inx_match.group('inx') if inx_match else 0,
                   str_area,
                   str_author,
                   element_img.get('alt'),
                   element_a.get('href'),
                   element_img.get('src'))
    return data

def writeData(data, dt):
    i_inx = 0
    i_area = 1
    i_author = 2
    i_description = 3
    i_url = 4
    i_img_url = 5
    
    data_filename = 'data.csv'
    if os.path.exists(data_filename):
        df = pd.read_csv(data_filename)
    else:
        df = pd.DataFrame(np.empty(0, dtype = dt))

    for line in data:
        imgdatas = []
        if np.all(df['inx'] != line[i_inx]):
            line[i_url] = addHttpScheme(line[i_url])
            line[i_img_url] = addHttpScheme(line[i_img_url])

            r = requests.get(line[i_img_url])
            imgdata = r.content
            
            with open('img/%s.jpg' % line[i_inx], 'wb') as fout:
                fout.write(imgdata)

            imgdatas.append(imgdata)
        
            text = '%s(%s) - %s %s' % (line[i_description],
                                       line[i_author],
                                       line[i_area],
                                       line[i_url])
            print(text)
            postTwitter(text, imgdatas)
            
    df = pd.concat([df, pd.DataFrame(data)])
    df = df.drop_duplicates('inx')

    df.to_csv(data_filename, index=False)

def postTwitter(text, imgdatas = []):
    consumer_key = 'UtVxSquH0tf0iKQpvOha7nFzg'
    consumer_secret = 'eI2pQUz2t2bVkFwOQg04ztw81Xyf5BNjRtNlt26uMWqBZWDU36'
    
    twitter_creds = os.path.expanduser('~/.secret/guru_tabi_twitter')
    if not os.path.exists(twitter_creds):
        twitter.oauth_dance('guru_tabi', consumer_key, consumer_secret, twitter_creds)

    oauth_token, oauth_secret = twitter.read_token_file(twitter_creds)
    
    t_auth = twitter.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
    t = twitter.Twitter(auth = t_auth)

    if imgdatas:
        img_ids = []
        for imgdata in imgdatas:
            img_upload = twitter.Twitter(domain='upload.twitter.com', auth = t_auth)
            img_id = img_upload.media.upload(media = imgdata)['media_id_string']
            img_ids.append(img_id)
    t.statuses.update(status = text, media_ids = ','.join(img_ids))

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
    print('guru_tabi v0.1')

main()
