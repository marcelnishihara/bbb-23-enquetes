import requests


url = ''
response = requests.get(
    url=url,
    headers={})

log = {
    'status_code': response.status_code,
    'text': response.text
}

print(log)
