import json
import configparser
import datetime
import tweepy
import csv
import numpy as np
from requests_oauthlib import OAuth1Session

# twitter developer api 연결하기 위한 key값 
def authTwitter():
    api_key = 'PmeYdimCGuvE3y5NwjmYEq1xg'
    api_secret_key = '3yNAHkyRj72Fxo7DKHTKSzf61OAmdJ8ZKPl4GzPrykl37N3hih'
    access_token ='1315675049454575617-9FeTS56XAzkbsoY372G43V6clXWnN9'
    access_secret_token = 'T6NEGRVMBBjbKxtMMYK7WdAu7WunIPk2mLWjH4PR1eXce'

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth, wait_on_rate_limit = True) # API利用制限にかかった場合、解除まで待機する
    return(api)

# csvfile에 수집했던 data 저장 
def csvfile(result):
    # r = 読み取り、 w = 上書き、　a = 追記
    with open('./tweet_data/kyo-to/kyotopi_1101_1110.csv','w',encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in result:
            writer.writerow(i)

# twitter로부터 data수집 
def getTweetbySearch():
    #result = np.array([])
    result = [[0] * 6 for i in range(6000)]
    api = authTwitter()

    #sratchStr = tweet_keyword + 기간 + ' exclude:retweets'
    #기간은 최근 1주일 밖에 못함
    sratchStr = "キョウトピ since:2020-11-01 until:2020-11-11 exclude:retweets"
    print('検索文字列 : '+ sratchStr)

    tweets = tweepy.Cursor(api.search, 
                           q = sratchStr,
                           include_entities = True, 
                           tweet_mode = 'extended', 
                           lang = 'ja').items()

    for i,tweet in enumerate(tweets):
        if i > len(result):
            exit
        else:
            result[i][0] = tweet.id
            result[i][1] = tweet.user.screen_name
            result[i][2] = tweet.created_at
            result[i][3] = tweet.full_text
            result[i][4] = tweet.favorite_count
            result[i][5] = tweet.retweet_count
    csvfile(result)

getTweetbySearch()
