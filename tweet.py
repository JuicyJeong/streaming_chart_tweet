import tweepy
import pandas as pd
from datetime import datetime
import json

from bs import chart_to_df
from bs import search_by_title
from bs import serach_by_artist

# with open('api_info.json', 'r') as file:
#     json_data = json.load(file)
    
# ############################DO NOT CHANGE##################################
# API_KEY = json_data['API_KEY']
# API_SECRET = json_data['API_SECRET']
# ACCESS_KEY = json_data['ACCESS_KEY']
# ACCES_SECRET = json_data['ACCES_SECRET']
# ############################DO NOT CHANGE##################################

# # #########################INIT############################
# auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
# auth.set_access_token(ACCESS_KEY,ACCES_SECRET)

# api = tweepy.API(auth)
# try:
#     api.verify_credentials()
#     print("Twitter api pass. Ready to tweet!")
# except:
#     print("Twitter api fail. call JUICY")
# # #########################INIT############################

# now = datetime.now()
# year = now.year
# month_raw = now.month
# day_raw = now.day
# hour_raw = now.hour
# month = f'{month_raw:02d}'
# day = f'{day_raw:02d}'
# hour = f'{hour_raw:02d}'


def post_tweet(contents,API_KEY,API_SECRET,ACCESS_KEY,ACCES_SECRET,BEARER_TOKEN):
    #auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
    #auth.set_access_token(ACCESS_KEY,ACCES_SECRET)
    #api = tweepy.API(auth)
    
    #api.update_status(contents)
    client = tweepy.Client(bearer_token=BEARER_TOKEN
                           , consumer_key=API_KEY
                           , consumer_secret=API_SECRET
                           , access_token=ACCESS_KEY
                           , access_token_secret=ACCES_SECRET)
    
    client.create_tweet(text=contents)



#사이트와 노래 제목을 입력하면, 그 사이트에서의 노래의 순위값들을 반환합니다. 반환 값은 그 노래에 대한 정보 트윗 값.
def generate_tweet_content(site_name, chart_category, site_chart, title_keyword):
    # 여기를 파일로 정리할 수 있나...?


    site_line = '' #초기화 한번 해줘야지 에러가 안남.
    if site_name == 'melon':
        if chart_category == 'top100':
            site_line = '💚멜론TOP100'
        elif chart_category == 'hot100-d100':
            site_line = '💚멜론HOT100(100일)'
        elif chart_category == 'newest-w1':
            site_line = '💚멜론최신차트(1주)'
        elif chart_category == 'newest-w4':
            site_line = '💚멜론최신차트(4주)'
        elif chart_category == 'realtime':
            site_line = '💚멜론실시간차트'
        elif chart_category == 'daily':
            site_line = '💚멜론일간차트'


    elif site_name =='bugs':
        if chart_category == 'realtime':
            site_line = '🧡벅스실시간차트'
        elif chart_category == 'daily':
            site_line = '🧡벅스일간차트'
        
    elif site_name == 'genie':
        if chart_category == 'realtime':
            site_line = '💙지니실시간차트'
        elif chart_category == 'daily':
            site_line = '💙지니일간차트'

    # elif site_name == 'youtube':
    #     if chart_category == 'track-weekly':
    #         site_line = '❤️유튜브주간인기곡'
    #     if chart_category == 'video-weekly':
    #         site_line = '❤️유튜브주간인기뮤직비디오'
        
    title_rank_result = search_by_title(site_chart, title_keyword)
    
    if len(title_rank_result) == 0: #검색 결과가 없을때
        tweet = f'{site_line}: 미진입\n'
        tweet_rank_only = f'{site_line}: 미진입\n'
        
    else: #검색 결과가 있을 때
        t_name = title_rank_result['곡 명'].iloc[0]
        t_rank = title_rank_result['순위'].iloc[0]
        t_is_up = title_rank_result['순위 변동'].iloc[0]
        if t_is_up == 'down':
            is_minus = '-'
        elif t_is_up == 'up':
            is_minus = '+'
        else:
            is_minus = ''
        t_rank_val = title_rank_result['순위 변동 값'].iloc[0]

        tweet = f'{site_line} {t_name}:{t_rank}위 ({is_minus}{t_rank_val}) \n' #곡 이름까지 붙어있는 트윗
        tweet_rank_only = f'{site_line} {t_rank}위 ({is_minus}{t_rank_val}) \n' # 곡 이름 없이 순위만 붙은 트윗

    return tweet_rank_only
if __name__== '__main__':
    #############################검색어를 입력해주세요##############################
	artist_keyword = '임영웅'
	title_keyword1 = '무지개'
    #############################검색어를 입력해주세요##############################

