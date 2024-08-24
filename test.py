import json
import time


with open('api_info.json', 'r') as file:
    json_data = json.load(file)

API_KEY = json_data['API_KEY']
API_SECRET = json_data['API_SECRET']
ACCESS_KEY = json_data['ACCESS_KEY']
ACCES_SECRET = json_data['ACCES_SECRET']

print(API_KEY)
print(API_SECRET)
print(ACCESS_KEY)
print(ACCES_SECRET)

from datetime import datetime

# 현재 날짜 가져오기
today = datetime.today()

# 현재 날짜의 연도, 주 번호, 요일 반환
year, week_number, weekday = today.isocalendar()

# 결과 출력
print(f"이번 주는 {year}년의 {week_number}번째 주입니다.")
