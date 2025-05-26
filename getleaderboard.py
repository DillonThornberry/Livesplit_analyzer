import requests
import json
import pandas as pd

sm64_url = 'https://www.speedrun.com/api/v1/games/o1y9wo6q/categories'
res = requests.get(sm64_url)
data = res.json()
data = data['data']
categories = []
for item in data[1:]:
    cat = {}
    id = item['id']
    cat['id'] = item['id']
    cat['name'] = item['name']
    cat['link'] = f'https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/{id}?embed=players'
    categories.append(cat)

n64 = 'w89rwelk'

leaderboards = []

for cat in categories:
    for emu in [True, False]:
        output = {}
        output['category'] = cat['name']
        output['emulator'] = emu

        link = cat['link']
        res = requests.get(f'{link}&platform={n64}&emulators={str(emu).lower()}')
        data = res.json()
        runs = data['data']['runs']
        
        df = pd.json_normalize(runs)
        print(df.columns)
        df.to_csv(f'./leaderboards/{cat["name"]} - {"emu" if emu else "n64"}.csv', index=False)
        




