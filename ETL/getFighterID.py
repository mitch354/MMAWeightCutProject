#Outputs the fighter's id into a json file
#This ID is needed to get individual fighter info from the http://ufc-data-api.ufc.com/api/v3/iphone/fighters/:id URL

import requests
import pandas as pd

fighters = requests.get('http://ufc-data-api.ufc.com/api/v3/iphone/fighters')
fighters_df = pd.DataFrame(fighters.json())
fighters_df = fighters_df[['first_name', 'last_name', 'weight_class', 'id']]
fighters_df = fighters_df.dropna()
fighters_df.id = fighters_df.id.astype(int)
fighters_df.to_json('fighters.json', orient='records')
