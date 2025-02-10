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
    auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCES_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter api pass. Ready to tweet!")
        return API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN

    except:
        print("Twitter api fail. call JUICY")
    # # #########################INIT############################


# 
def get_chart_data(chart_name, category_name): # 리턴값을 리스트로.[차트명, 카테고리명, df]
    chart_list = ['melon','genie','bugs','youtube']
    
    if chart_name in chart_list:
        chart_res = chart_to_df(chart_name, category_name)
        print('성공!')
        res_list = [chart_name, category_name, chart_res]
        return res_list
    else:
        print("잘못 입력된 차트명입니다. 다시 입력해주세요.")



# 이거 차트 입력 리스트로 받을까? 리스트[0] 차트명, 리스트[1] 카테고리, 리스트[2] df로 로드 합니다. 

def get_chart_data_AND_write_content(title_keyword, title_keyword_hashtag, chart_list):
     #시간별로 루프 도는 부분#####################################################################
    now = datetime.now()
    month_raw = now.month
    day_raw = now.day
    hour_raw = now.hour
    month = f'{month_raw:02d}'
    day = f'{day_raw:02d}'
    hour = f'{hour_raw:02d}'
    



    content_tweet = ""
    for i in range(len(chart_list)):
        current_chart = chart_list[i]

        tweet = generate_tweet_content(current_chart[0],current_chart[1],current_chart[2],title_keyword)
        
        content_tweet = content_tweet + tweet

    # print(content_tweet)

    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################
    tweet_title_info = f'#{title_keyword_hashtag} #{artist_keyword}\n ' #여기에 아티스트 해시태그를 입력.
    tweet_time_info = f'☆{month}/{day}  {hour}:00\n'
    

    # tweet_comment = "안녕하세요? 이 트윗은 트위터 자동 봇으로 작성된 트윗입니다."
    tweet_comment = ""
    ###########################트윗 내용 작성하는 구간. 맨 위의 타이틀은 직접 작성해주세요!#########################


    title_time_tweet_content = tweet_title_info + tweet_time_info
    
    total_content = content_tweet
    
    etc_tweet_content = tweet_comment

    final_tweet_content = title_time_tweet_content + total_content + etc_tweet_content
    return final_tweet_content










if __name__== '__main__':
    

    ''' 
    2024.08 사이트 url 카테고리 업데이트
    * 기본적인 url 구성
        가이섬.com/chart/{음원사이트이름}/{차트_카테고리이름}/{날짜}/{시간}
        이 포맷에 맞지 않는 url도 존재하지만 그건 제외하기로 함

    날짜, 시간은 현재 시간기준으로 입력됨.
    * 멜론 {melon} 차트 카테고리
        TOP100: top100
        HOT100(100일): hot100-d100
        최신차트(1주): newest-w1
        최신차트(4주): newest-w4
        실시간 차트: realtime
        일간 차트: daily
        

    * 지니 {genie} 차트 카테고리
        실시간 차트: realtime
        일간 차트: daily
        
    * 벅스 {bugs} 차트 카테고리
        실시간 차트: realtime
        일간 차트: daily

    * 유튜브 {youtube} 차트 카테고리
        주간 인기곡 차트: track-weekly
        주간 인기 뮤직비디오 차트: video-weekly

    '''
    
    title_keyword_list = ['Pump Up The Volume!'] # 여기에 곡명을 입력. 두개를 쓸 거면 쉼표로 작성.
    title_keyword_list_hashtag= ['Pump Up The Volume!'] # 여기에 곡명 해시태그를 입력
    artist_keyword = "PLAVE"


    API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN = init_twitter_api()

    
    # 받아올 차트들을 리스트로 정리합니다.
    total_list =[]
    content_0 = get_chart_data('melon','top100') # 리스트임
    content_1 = get_chart_data('bugs', 'daily')
    content_2 = get_chart_data('genie','realtime')
    content_3 = get_chart_data('youtube','track-weekly' ) #유튜브는 위크 기준으로 새로 입력해야함...
    # 귀찮으니 일단 보류. 

    total_list.append(content_0)
    total_list.append(content_1)
    total_list.append(content_2)
    total_list.append(content_3)


    for i in range(len(title_keyword_list)): #여러트윗을 하기 위해 반복 돌리는 구문

        # content =  "TEST TWEET."
        content =  get_chart_data_AND_write_content(title_keyword_list[i],title_keyword_list_hashtag[i],total_list)
        

        print('################################TWEETPART#################################')
        print(content)
        print('################################TWEETPART#################################')
        print(f'SYSTEM: {title_keyword_list[i]}의 트윗이 완료 되었습니다. 30초 후에 새로운 트윗을 작성합니다.')
 
    	#tweetpart. 마지막까지 확인 또 확인. 마지막에 주석 풀기
        # post_tweet(content,API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN)
        # random_sec = random.randint(15, 40)

        # time.sleep(random_sec)






