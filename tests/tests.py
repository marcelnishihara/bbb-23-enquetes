'''
Module tests
'''

import json
import requests

LOCALHOST = ''

response = requests.get(
    url=LOCALHOST,
    timeout=10,
    headers={
        'projectUUID': '',
        'tweet': '',
        'pollIndex': '',
        'housematesNumber': '',
        'counterLimit': '',
        'sourceWebPage': '',
        'sourcesJsonFile': ''})

log = {
    'status_code': response.status_code, 
    'text': json.loads(s=response.text)}

print(json.dumps(obj=log, indent=4))
