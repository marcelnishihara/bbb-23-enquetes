'''
Module tests
'''

import requests


LOCALHOST = 'http://127.0.0.1:8080'

response = requests.get(
    url=LOCALHOST,
    headers={
        'projectUUID' : '123465'
    })

log = {
    'status_code': response.status_code,
    'text': response.text
}

print(log)
