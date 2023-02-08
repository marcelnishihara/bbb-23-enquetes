'''
Module tests
'''


import requests

LOCALHOST = ''

response = requests.get(
    url=LOCALHOST,
    timeout=10,
    headers={})

log = {
    'status_code': response.status_code,
    'text': response.text
}

print(log)
