# Outputs the fighter's info into a json file
# ID is needed to get individual fighter info from the http://ufc-data-api.ufc.com/api/v3/iphone/fighters/:id URL

import requests
import pandas as pd
import time
from lxml import html

# For changing the names returned by the API
weight_dict = {
    "Women_Strawweight": "Women's Strawweight",
    "Women_Flyweight": "Women's Flyweight",
    "Women_Bantamweight": "Women's Bantamweight",
    'Women_Featherweight': "Women's Featherweight",
    "Flyweight": "Flyweight",
    "Bantamweight": "Bantamweight",
    "Featherweight": "Featherweight",
    "Lightweight": "Lightweight",
    "Welterweight": "Welterweight",
    "Middleweight": "Middleweight",
    "Light_Heavyweight": "Light Heavyweight",
    "Heavyweight": "Heavyweight",
}

# scrapes the html to find the reach of a fighter
def getFighterReach(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)
    reach = tree.xpath('//td[@id="fighter-reach"]/text()')
    if (reach):
        return int(reach[0][:-1])
    else:
        return 0

# returns a json list of all fighters with their info
fighters = requests.get('http://ufc-data-api.ufc.com/api/v3/iphone/fighters')

# put json data into a Pandas dataframe and keep only a few columns
fighters_df = pd.DataFrame(fighters.json())
fighters_df["name"] = fighters_df["first_name"] + " " + fighters_df["last_name"]
fighters_df = fighters_df[['name', 'weight_class', 'id', 'link']]
fighters_df = fighters_df.dropna()
fighters_df.id = fighters_df.id.astype(int)
fighters_df = fighters_df.reset_index(drop=True)
# Columns to be added through additional API calls and web scraping
fighters_df['dob'] = ""
fighters_df['height'] = ""
fighters_df['reach'] = ""

# This will take 10+ minutes, need to sleep between API calls to avoid multiple
# successive calls causing some router to drop requests
for i in range(0,fighters_df.shape[0]):
    fighter = requests.get('http://ufc-data-api.ufc.com/api/v3/iphone/fighters/' + str(fighters_df.iloc[i]['id']) + '.json')
    info = fighter.json()
    fighters_df.set_value(i, 'dob', info['dob'])
    fighters_df.set_value(i, 'height', info['height'])
    time.sleep(1)

# This will take several minutes
fighters_df['reach'] = fighters_df['link'].apply(getFighterReach)
# Impute data, not all fighter profiles contain reach info. Height is a good estimation.
fighters_df.loc[fighters_df['reach'] == 0, 'reach'] = fighters_df['height']
# A few fighters don't have a height listed, remove these and reset the index
fighters_df = fighters_df[fighters_df.height != 0]
fighters_df = fighters_df.reset_index(drop=True)

# drop extra columns, and adjust a few column values / datatypes
fighters_df = fighters_df.drop(['link'], axis=1)
fighters_df['weight_class'] = fighters_df['weight_class'].apply(lambda x: weight_dict[x])
fighters_df['dob'] = pd.to_datetime(fighters_df['dob'])

# Save dataframe to a json file
fighters_df.to_json('fighters.json', orient='records')
