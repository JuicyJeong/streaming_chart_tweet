import json

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