"""
Functional test
"""

import requests
import json

url = 'http://localhost:6543/'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

print "/lobby"
r = requests.get(url + 'lobby').json()
print r

print
print "/join"
data = {'scene':'basement', 'avatar':'anxious'}
r = requests.post(url + 'join', data=json.dumps(data), headers=headers).json()
print r

print
print "/question"
token = r['token']
headers['Authorization'] = 'Bearer {}'.format(token)
r = requests.get(url + 'question', headers=headers).json()
print r

print
print "/respond"
data = {'question':'0', 'response':'0'}
r = requests.post(url + "respond", data=json.dumps(data), headers=headers).json()
print r

print
print "/question"
r = requests.get(url + 'question', headers=headers).json()
print r

print
print "/respond"
data = {'question':'1', 'response':'0'}
r = requests.post(url + "respond", data=json.dumps(data), headers=headers).json()
print r

print
print "/question"
r = requests.get(url + 'question', headers=headers).json()
print r


print
print "/responses"
data = {'question': '0'}
r = requests.post(url + "responses", data=json.dumps(data), headers=headers).json()
print r

print
print "/responses"
data = {'question': '1'}
r = requests.post(url + "responses", data=json.dumps(data), headers=headers).json()
print r
