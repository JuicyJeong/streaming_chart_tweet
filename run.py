import tweepy
import pandas as pd
import time
from datetime import datetime
import json
import random

from bs import chart_to_df
from bs import search_by_title
from bs import serach_by_artist
from tweet import post_tweet
from tweet import generate_tweet_content

#1. 트위터 api 값 받아오고 초기화.
def init_twitter_api():

    # with open('/home/juicy/proj/streaming_chart_tweet/api_info.json', 'r') as file:
    #     json_data = json.load(file)
    with open('api_info_JUICY.json', 'r') as file:
        json_data = json.load(file)
    ############################DO NOT CHANGE##################################
    API_KEY = json_data['API_KEY']
    API_SECRET = json_data['API_SECRET']
    ACCESS_KEY = json_data['ACCESS_KEY']
    ACCES_SECRET = json_data['ACCESS_SECRET']
    BEARER_TOKEN = json_data['BEARER_TOKEN']
    ############################DO NOT CHANGE##################################

    # #########################INIT############################
    #auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
    #auth.set_access_token(ACCESS_KEY,ACCES_SECRET)

    #api = tweepy.API(auth)
    try:
        #api.verify_credentials()
        print("Twitter api pass. Ready to tweet!")
        return API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN

    except:
        print("Twitter api fail. call JUICY")
    # # #########################INIT############################



def get_chart_data():
    # 차트를 불러옵니다
    print('멜론 차트 가져오는중...')
    # melon_chart_realtime = chart_to_df('melon','realtime')
    #melon_chart_daily = chart_to_df('melon','daily')
    melon_chart_top100 = chart_to_df('melon','top100')
    melon_chart_hot100 = chart_to_df('melon','hot100')
    print('성공!')


    print('벅스 차트 가져오는 중...')
    bugs_chart_realtime = chart_to_df('bugs','realtime')
    #bugs_chart_daily = chart_to_df('bugs','daily')
    # 벅스는 top100은 없네요...
    print('성공!')

    print('지니 차트 가져오는 중...')
    genie_chart_realtime = chart_to_df('genie','realtime')
    #genie_chart_daily = chart_to_df('genie','daily')
    # 지니도 top100은 없네...
    print('성공!')

    #리턴값으로 갖고오고 싶은 차트들을 설정하기.
    return melon_chart_top100,melon_chart_hot100,bugs_chart_realtime,genie_chart_realtime




# 여기에서도 들고올 차트들을 정합성이 맞게 입력값을 설정하기.
def get_chart_data_AND_write_content(title_keyword, title_keyword_hashtag, melon_chart_top100,melon_chart_hot100,bugs_chart_realtime,genie_chart_realtime):
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
    melon_data_top100 = generate_tweet_content('melon', 'top100', melon_chart_top100, title_keyword)
    #melon_data_daily = generate_tweet_content('melon', 'daily', melon_chart_daily, title_keyword)
    melon_data_hot100 = generate_tweet_content('melon', 'hot100', melon_chart_hot100, title_keyword)

    bugs_data_realtime = generate_tweet_content('bugs', 'realtime',bugs_chart_realtime,title_keyword)
    #bugs_data_daily = generate_tweet_content('bugs','daily',bugs_chart_daily,title_keyword)

    genie_data_realtime = generate_tweet_content('genie', 'realtime', genie_chart_realtime,title_keyword)
    #genie_data_daily = generate_tweet_content('genie', 'daily', genie_chart_daily,title_keyword)
    #########################음원사이트, 차트별로 트윗 내용 가져오기#########################


    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################
    tweet_title_info = f'#{title_keyword_hashtag} #이세계아이돌\n ' #여기에 아티스트 해시태그를 입력.
    tweet_time_info = f'☆{month}/{day}  {hour}:00\n'
    # tweet_content1 = melon_data_realtime
    tweet_content2 = melon_data_top100
    tweet_content3 = melon_data_hot100
    tweet_content4 = bugs_data_realtime
    #tweet_content5 = bugs_data_daily
    tweet_content6 = genie_data_realtime
    #tweet_content7 = genie_data_daily

    # tweet_comment = "안녕하세요? 이 트윗은 트위터 자동 봇으로 작성된 트윗입니다."
    tweet_comment = ""
    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################


    title_time_tweet_content = tweet_title_info + tweet_time_info
    # melon_tweet_content = tweet_content1 + tweet_content2 + tweet_content3
    melon_tweet_content = tweet_content2 + tweet_content3
    bugs_tweet_content = tweet_content4 #+ tweet_content5
    genie_tweet_content = tweet_content6 #+ tweet_content7
    etc_tweet_content = tweet_comment

    final_tweet_content = title_time_tweet_content + melon_tweet_content + bugs_tweet_content + genie_tweet_content + etc_tweet_content
    return final_tweet_content










if __name__== '__main__':
    
    title_keyword_list = ['KIDDING'] # 여기에 곡명을 입력. 두개를 쓸 거면 쉼표로 작성.
    title_keyword_list_hashtag= ['KIDDING'] # 여기에 곡명 해시태그를 입력


    # API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN = init_twitter_api()

    melon_chart_top100,melon_chart_hot100,bugs_chart_realtime,genie_chart_realtime = get_chart_data()
    for i in range(len(title_keyword_list)): #여러트윗을 하기 위해 반복 돌리는 구문

        # content =  "TEST TWEET."
        content =  get_chart_data_AND_write_content(title_keyword_list[i],title_keyword_list_hashtag[i],melon_chart_top100,melon_chart_hot100,bugs_chart_realtime,genie_chart_realtime)
        

        print('################################TWEETPART#################################')
        print(content)
        print('################################TWEETPART#################################')
        print(f'SYSTEM: {title_keyword_list[i]}의 트윗이 완료 되었습니다. 30초 후에 새로운 트윗을 작성합니다.')
 
    	#tweetpart. 마지막까지 확인 또 확인. 마지막에 주석 풀기
        # post_tweet(content,API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN)
        random_sec = random.randint(15, 40)

        time.sleep(random_sec)






