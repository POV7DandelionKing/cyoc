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
data = {'scene':'basement', 'avatar':'angry'}
r = requests.post(url + 'join', data=json.dumps(data), headers=headers).json()
print r
token = r['token']
headers['Authorization'] = 'Bearer {}'.format(token)

print
print "/start"
r = requests.get(url + 'start', data=json.dumps(data), headers=headers).json()
print r

print
print "/respond"
data = {'question':'0', 'response':'0'}
r = requests.post(url + "respond", data=json.dumps(data), headers=headers).json()
print r

print
print "/respond"
data = {'question':'1', 'response':'0'}
r = requests.post(url + "respond", data=json.dumps(data), headers=headers).json()
print r
