import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
'''
가이섬 홈페이지의 실시간 음원차트 데이터를 가져오는 스크립트 입니다.
홈페이지의 업데이트 시간이 조금 있으므로 정각에 바로 실행 시키면 페이지가 로딩되지 않아 오류가 발생합니다.
3~5분의 대기시간을 가진 후, 실행부탁드립니다. 
'''
#0930. 아직 업데이트가 완료되지 않음. 좀 더 크롤링 하는 것을 따로 작업해봐야할듯.
now = datetime.now()
year = now.year
month_raw = now.month
day_raw = now.day
hour_raw = now.hour
month = f'{month_raw:02d}'
day = f'{day_raw:02d}'
hour = f'{hour_raw:02d}'
#print(year,month,day,hour)
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
    

* 지니 {genie} 차트 카테고리
    실시간 차트: realtime
    
* 벅스 {bugs} 차트 카테고리
    실시간 차트: realtime

* 유튜브 {youtube} 차트 카테고리
    주간 인기곡 차트: track-weekly
    주간 인기 뮤직비디오 차트: video-weekly

'''

def chart_to_df(striming_list,category):

    now = datetime.now()
    year = now.year
    month_raw = now.month
    day_raw = now.day
    hour_raw = now.hour
    month = f'{month_raw:02d}'
    day = f'{day_raw:02d}'
    yesterday = f'{day_raw-2:02d}'
    hour = f'{hour_raw:02d}'
    # print(year,month,day,hour)

    base_path = 'https://xn--o39an51b2re.com/'


    result_df = pd.DataFrame()
    #일간차트의 경우, 오늘 날짜에 대해서는 업데이트가 진행되지 않았기 때문에, 하루 전것의 데이터를 가져와야함. url형식도 다르니 따로 선업합니다.
    if category =='daily':
        url = base_path+'chart/'+striming_list+'/'+category+'/'+str(year) + str(month) + str(yesterday)
    else:
        url = base_path+'chart/'+striming_list+'/'+category+'/'+str(year) + str(month) + str(day)+ "/" + str(hour)
    # print(url)
    #url = 'https://xn--o39an51b2re.com/melon/chart/realtime/20230608/13'
    # 웹 페이지에 접속하여 HTML 가져오기
    print(url)

    response = requests.get(url)
    html = response.text

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    
    

    for i in range(1,101): 
        chart_to_dict = {}

        song_rank = i # 곡 순위 
        # 첫번째 i가 랭크 정보가 아니라... 이상한 라인이라서 2번째부터 101번째까지 긁어옵니다. 10.01
        song_artist_raw = soup.select(f"#chart-table-content > tbody > tr:nth-child({song_rank+1}) > td.subject > p:nth-child(2)") #태그 까지 들고옵니다 
        song_title_raw = soup.select(f"#chart-table-content > tbody > tr:nth-child({song_rank+1}) > td.subject > p:nth-child(1)")
        print(f"{song_rank}'위:{song_title_raw}")
        song_artist = song_artist_raw[0].text # 태그를 텍스트값만 깔끔하게 갖고 옵니다.
        song_title = song_title_raw[0].text
        song_ranking_updown = soup.select(f"#chart-table-content > tbody > tr:nth-child({song_rank+1}) > td.ranking > p.change > span") # 태그에 업,다운이 있고 값이 있어서 따로 밑의 조건문에서 처리.

        # 순위 변동이 있을시, 그 값을 따로 저장합니다.
        #이 값들은 반복 돌때마다 초기화 해야함
        up_down = "-"
        up_down_val = 0

        str_updown = str(song_ranking_updown[0])[12:-7] # "down">4
        if 'down' in str_updown:
            # print('순위가 내려갔습니다.')
            dir_val = str_updown.split(">")
            # print(dir_val[0])
            # print(dir_val[1])
            up_down = dir_val[0].strip('"')
            up_down_val = dir_val[1]
        elif 'up' in str_updown:
            #print('순위가 올라갔습니다.')
            dir_val = str_updown.split(">")
            # print(dir_val[0])
            # print(dir_val[1])
            up_down = dir_val[0].strip('"')
            up_down_val = dir_val[1]
        else:
            #print("순위에 변동이 없습니다.")
            pass

      
        if up_down_val ==0:
            #print(f"순위:{song_rank}, \n아티스트: {song_artist}, \n곡 명: {song_title}, \n순위 변동: -")
            chart_to_dict={'순위':song_rank, '아티스트':song_artist, '곡 명':song_title, '순위 변동': '-', '순위 변동 값': '-'}

        else:
            #print(f"순위:{song_rank}, \n 아티스트: {song_artist}, \n 곡 명: {song_title}, \n 순위 변동: {up_down}->{up_down_val}")
            chart_to_dict={'순위':song_rank, '아티스트':song_artist, '곡 명':song_title, '순위 변동': up_down, '순위 변동 값':up_down_val}

        add_df = pd.DataFrame(chart_to_dict,index=[i])
        result_df = pd.concat([result_df,add_df])
    # print(result_df)
    return result_df

def search_by_title(chart_name, keyword):
    result = chart_name[chart_name['곡 명']==keyword]
    #print(result)
    return result

def serach_by_artist(chart_name,keyword):
    result = chart_name[chart_name['아티스트']==keyword]
    num_of_titles = len(result)
    
    # print(result)
    return result
   


if __name__== '__main__':
    ##########################################################################
    #############################키워드를 입력해주세요##############################
    ##########################################################################
    '''
    실시간 차트에 올라온 텍스트 그대로 입력해야 검색이 됩니다.'''
    artist_keyword = '무지개'
    title_keyword = '무지개'

    ##########################################################################
    #############################키워드를 입력해주세요##############################
    ##########################################################################

    
    # bugs_chart = chart_to_df('bugs')
    melon_chart = chart_to_df('melon','top100')
    # genie_chart = chart_to_df('genie')

    # bugs_chart.to_csv(f'chart/벅스 차트{year}{month}{day}_{hour}.csv', encoding='utf-8')
    melon_chart.to_csv(f'멜론 차트_{year}{month}{day}_{hour}.csv', encoding='utf-8')
    # genie_chart.to_csv(f'chart/지니 차트{year}{month}{day}_{hour}.csv', encoding='utf-8')
    
    # 벅스 차트
    # bugs_search_title = search_by_title(bugs_chart,title_keyword)
    #bugs_search_artist = serach_by_artist(bugs_chart,title_keyword)

    # 멜론 차트
    # melon_search_title = search_by_title(melon_chart,title_keyword)


    #melon_search_artist = serach_by_artist(melon_chart,title_keyword)
    # 지니 차트
    # genie_search_title = search_by_title(genie_chart,title_keyword)
    #genie_search_title = serach_by_artist(genie_chart,title_keyword)

