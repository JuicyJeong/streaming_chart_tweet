import tweepy
import pandas as pd
import time
from datetime import datetime
import json

from bs import chart_to_df
from bs import search_by_title
from bs import serach_by_artist
from tweet import post_tweet
from tweet import generate_tweet_content

#1. 트위터 api 값 받아오고 초기화.
def init_twitter_api():

    with open('api_info.json', 'r') as file:
        json_data = json.load(file)
        
    ############################DO NOT CHANGE##################################
    API_KEY = json_data['API_KEY']
    API_SECRET = json_data['API_SECRET']
    ACCESS_KEY = json_data['ACCESS_KEY']
    ACCES_SECRET = json_data['ACCES_SECRET']
    ############################DO NOT CHANGE##################################

    # #########################INIT############################
    auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCES_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter api pass. Ready to tweet!")
    except:
        print("Twitter api fail. call JUICY")
    # # #########################INIT############################

artist_keyword = 'PLAVE'
title_keyword1 = '여섯 번째 여름'


def get_chart_data():
    # 차트를 불러옵니다
    print('멜론 차트 가져오는중...')
    # melon_chart_realtime = chart_to_df('melon','realtime')
    melon_chart_daily = chart_to_df('melon','daily')
    # melon_chart_top100 = chart_to_df('melon','top100')
    melon_chart_hot100 = chart_to_df('melon','hot100')
    print('성공!')


    print('벅스 차트 가져오는 중...')
    bugs_chart_realtime = chart_to_df('bugs','realtime')
    bugs_chart_daily = chart_to_df('bugs','daily')
    # 벅스는 top100은 없네요...
    print('성공!')

    print('지니 차트 가져오는 중...')
    genie_chart_realtime = chart_to_df('genie','realtime')
    genie_chart_daily = chart_to_df('genie','daily')
    # 지니도 top100은 없네...
    print('성공!')

    return melon_chart_daily,melon_chart_hot100,bugs_chart_realtime,bugs_chart_daily,genie_chart_realtime,genie_chart_daily






def get_chart_data_AND_write_content(title_keyword, title_keyword_hashtag, melon_chart_daily,melon_chart_hot100,bugs_chart_realtime,bugs_chart_daily,genie_chart_realtime,genie_chart_daily):
     #시간별로 루프 도는 부분#####################################################################
    now = datetime.now()
    month_raw = now.month
    day_raw = now.day
    hour_raw = now.hour
    month = f'{month_raw:02d}'
    day = f'{day_raw:02d}'
    hour = f'{hour_raw:02d}'
    
 
    

    ########################음원사이트, 차트별로 트윗 내용 가져오기#########################
    # melon_data_realtime = generate_tweet_content('melon', 'realtime',melon_chart_realtime, title_keyword1)
    # melon_data_daily = generate_tweet_content('melon', 'daily', melon_chart_daily, title_keyword)
    melon_data_daily = generate_tweet_content('melon', 'daily', melon_chart_daily, title_keyword)
    melon_data_top100 = generate_tweet_content('melon', 'hot100', melon_chart_hot100, title_keyword)

    bugs_data_realtime = generate_tweet_content('bugs', 'realtime',bugs_chart_realtime,title_keyword)
    bugs_data_daily = generate_tweet_content('bugs','daily',bugs_chart_daily,title_keyword)

    genie_data_realtime = generate_tweet_content('genie', 'realtime', genie_chart_realtime,title_keyword)
    genie_data_daily = generate_tweet_content('genie', 'daily', genie_chart_daily,title_keyword)
    #########################음원사이트, 차트별로 트윗 내용 가져오기#########################


    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################
    tweet_title_info = f'#{title_keyword_hashtag} #PLAVE\n '
    tweet_time_info = f'☆{month}/{day}  {hour}:00\n'
    # tweet_content1 = melon_data_realtime
    tweet_content2 = melon_data_daily
    tweet_content3 = melon_data_top100
    tweet_content4 = bugs_data_realtime
    tweet_content5 = bugs_data_daily
    tweet_content6 = genie_data_realtime
    tweet_content7 = genie_data_daily

    # tweet_comment = "안녕하세요? 이 트윗은 트위터 자동 봇으로 작성된 트윗입니다."
    tweet_comment = ""
    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################


    title_time_tweet_content = tweet_title_info + tweet_time_info
    # melon_tweet_content = tweet_content1 + tweet_content2 + tweet_content3
    melon_tweet_content = tweet_content2 + tweet_content3
    bugs_tweet_content = tweet_content4 + tweet_content5
    genie_tweet_content = tweet_content6 + tweet_content7
    etc_tweet_content = tweet_comment

    final_tweet_content = title_time_tweet_content + melon_tweet_content + bugs_tweet_content + genie_tweet_content + etc_tweet_content
    return final_tweet_content










if __name__== '__main__':
    interval = 120  # 5분을 초로 환산
    start_hour = 6  # 시작 시간 (6시)
    end_hour = 23  # 종료 시간 (23시)

    artist_keyword = 'PLAVE'
    title_keyword1 = '여섯 번째 여름'
    title_keyword_list = ['왜요 왜요 왜?','여섯 번째 여름', 'I Just Love Ya', 'Dear. PLLI']
    title_keyword_list_hashtag= ['왜요_왜요_왜?🌿','여섯_번째_여름🌿', 'I_Just_Love_Ya🌿', 'Dear_PLLI🌿']


    # init_twitter_api()


    melon_chart_daily,melon_chart_hot100,bugs_chart_realtime,bugs_chart_daily,genie_chart_realtime,genie_chart_daily = get_chart_data()
    for i in range(len(title_keyword_list)):

        content =  get_chart_data_AND_write_content(title_keyword_list[i],title_keyword_list_hashtag[i],melon_chart_daily,melon_chart_hot100,bugs_chart_realtime,bugs_chart_daily,genie_chart_realtime,genie_chart_daily)

        print('################################TWEETPART#################################')
        print(content)
        print('################################TWEETPART#################################')
    
    #tweet
    # post_tweet(final_tweet_content,API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET)