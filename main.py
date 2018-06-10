#!/usr/bin/python3
# coding: utf-8

import time
import json

from requests_oauthlib import OAuth1Session
import slackweb

# URLs for Twitter API
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authorize'
# Consumer key
CK = ''
# Consumer secret
CS = ''
# Access token
AT = ''
# Access token secret
AS = ''

# Webhook URL for slack
webhook_url = ''

def parse_date(date):
    mtom = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    month = mtom[date[4:7]]
    dd = date[8:10]
    hh = date[11:13]
    mm = date[14:16]
    ss = date[17:19]
    yyyy = date[26:30]
    return [yyyy,month,dd,hh,mm,ss]

def cmp_date(date1,date2):
    if date1[0]>date2[0] or (date1[0]==date2[0] and date1[1]>date2[1]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]>date2[2]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]==date2[2] and date1[3]>date2[3]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]==date2[2] and date1[3]==date2[3] and date1[4]>date2[4]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]==date2[2] and date1[3]==date2[3] and date1[4]==date2[4] and date1[5]>date2[5]):
        return True
    else:
        return False

def cond_text(text):
    if text[:3] == 'You':
        return True
    else:
        return False

def write_date(date):
    with open("date.txt","w") as f:
        f.write(date[0]+date[1]+date[2]+date[3]+date[4]+date[5])

def read_date():
    date = []
    with open("date.txt","r") as f:
        t = f.read()
        date.append(t[:4])
        date.append(t[4:6])
        date.append(t[6:8])
        date.append(t[8:10])
        date.append(t[10:12])
        date.append(t[12:14])
    return date

def main():
    twitter = OAuth1Session(CK,CS,AT,AS)
    slack = slackweb.Slack(url=webhook_url)
    url_get = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    params_id = {'screen_name': 'hoge'}
    params_get = {'screen_name':'hoge','count':100}


    recentDate = read_date()
    while True:
        req = twitter.get(url_get,params=params_get)
        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tw in search_timeline[::-1]:
                if cond_text(tw['text']):
                    if cmp_date(parse_date(tw['created_at']),recentDate):

                        slack.notify(text=tw['text'])

                        if 'extended_entities' in tw.keys():
                            img_urls = []
                            for i in range(len(tw['extended_entities']['media'])):
                                img_urls.append(tw['extended_entities']['media'][i]['media_url'])
                            for i in range(len(img_urls)):
                                slack.notify(text=img_urls[i])

                        recentDate = parse_date(tw['created_at'])
                        write_date(recentDate)
        else:
            print("ERROR: %d" % req.status_code)
        time.sleep(60)


if __name__ == '__main__':
    main()
