# Outputs relevant fight info into a json file

import requests
from lxml import html
import pandas as pd
import numpy as np
import time

# Translate weightclass returned from API into a numeric value

weight_dict = {
    "Catch Weight": 0,
    "Women's Strawweight": 116,
    "Women's Flyweight": 126,
    "Women's Bantamweight": 136,
    "Women's Featherweight": 146,
    "Flyweight": 126,
    "Bantamweight": 136,
    "Featherweight": 146,
    "Lightweight": 156,
    "Welterweight": 171,
    "Middleweight": 186,
    "Light Heavyweight": 206,
    "Heavyweight": 266,
    "Open Weight": 0,
    "Super Heavyweight": 0
}

# Needs the output file produced from getFighterInfo.py

fighters = pd.read_json('fighters.json')

fights = pd.DataFrame(columns=['fighter_id','date', 'weigh_in', 'won', 'weight_limit'])

for i in range(0,len(fighters)):
    time.sleep(1)
    fighter_id = fighters.iloc[i]['id']
    fighter_data = requests.get('http://ufc-data-api.ufc.com/api/v3/iphone/fighters/' + str(fighter_id) + '.json')
    fighter_data = fighter_data.json()
    if ('fights' in fighter_data):
        num_fights = len(fighter_data['fights'])
        for j in range(0, int(num_fights)):
            if ('UFC' in (fighter_data['fights'][j]['Event']['Name']).upper()):
                date = fighter_data['fights'][j]['Event']['Date']
                weigh_in = fighter_data['fights'][j]['WeighIn']
                won = fighter_data['fights'][j]['Result']['Outcome']
                weight_limit = fighter_data['fights'][j]['WeightClass']['Description']
                fights.loc[len(fights)] = [fighter_id, date, weigh_in, won, weight_limit]

fights = fights.dropna()
fights['max_weight'] = fights['weight_limit'].apply(lambda x: weight_dict[x])
fights['weigh_in'] = pd.to_numeric(fights['weigh_in'])
fights = fights[fights['max_weight'] != 0]
fights = fights.reset_index(drop=True)

fights.to_json('fights.json', orient='records')
