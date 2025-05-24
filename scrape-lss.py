import requests
import json 
from bs4 import BeautifulSoup as bs
from time import sleep

def make_download_url(user, cat):
    base = 'https://d2c9jb6sm40v74.cloudfront.net/'
    return f'{base}{user}/Super+Mario+64-{cat}.lss'


html = open('lb.html', 'r').read()

soup = bs(html, 'html.parser')
hrefs = [a['href'] for a in soup.find_all('a', href=True)]

for href in hrefs:
    texts = href.split('/')
    user = texts[1]
    cat = texts[3]
    cat = cat.replace('%20', '+')
    cat = cat.split('%')[0]
    url = make_download_url(user, cat)

    res = requests.get(url)
    data = res.content
    if data.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n<Error>'):
        print(f'Error downloading {user} {cat}')
        continue
    with open(f'./lss/no-lblj/no-lblj-{user}.lss', 'wb') as f:
        f.write(data)
    print(f'Downloaded {user} {cat}')
    sleep(1)
