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

# Gets the age that the fighter was for each fight
def getAge(row):
    fighter = fighters[fighters['id'] == row['fighter_id']]
    age = (row['date'] - fighter['dob'].iloc[0]).days
    age = age / 365.25
    return age


# Needs the output file produced from getFighterInfo.py
fighters = pd.read_json('fighters.json')
# Creates a dataframe that houses individual fight info
fights = pd.DataFrame(columns=['fighter_id','date', 'weigh_in', 'won', 'weight_limit'])

# Gets indivudal fight info by iterating through all fights from each fighter
for i in range(0,len(fighters)):
    time.sleep(1)
    fighter_id = fighters.iloc[i]['id']
    fighter_data = requests.get('http://ufc-data-api.ufc.com/api/v3/iphone/fighters/' + str(fighter_id) + '.json')
    fighter_data = fighter_data.json()
    # If a fighter is new and has no fights the fight attribute will be missing, must check
    if ('fights' in fighter_data):
        num_fights = len(fighter_data['fights'])
        # Iterate through each fight
        for j in range(0, int(num_fights)):
            if ('UFC' in (fighter_data['fights'][j]['Event']['Name']).upper()):
                date = fighter_data['fights'][j]['Event']['Date']
                weigh_in = fighter_data['fights'][j]['WeighIn']
                won = fighter_data['fights'][j]['Result']['Outcome']
                weight_limit = fighter_data['fights'][j]['WeightClass']['Description']
                # Add a row to the fights dataframe
                fights.loc[len(fights)] = [fighter_id, date, weigh_in, won, weight_limit]

# Compute additional columns, adjsut datatypes, drop rows with null values, etc
fights = fights.dropna()
fights['max_weight'] = fights['weight_limit'].apply(lambda x: weight_dict[x])
fights['weigh_in'] = pd.to_numeric(fights['weigh_in'])
fights['missed_weight'] = fights['weigh_in'] > fights['max_weight']
fights = fights[fights['max_weight'] != 0]
fights = fights[fights['weigh_in'] != 0]
fights['date'] = pd.to_datetime(fights['date'])
fights['age'] = fights.apply(getAge, axis=1)
fights = fights.reset_index(drop=True)

# Save dataframe to json file
fights.to_json('fights.json', orient='records')
