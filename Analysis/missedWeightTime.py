import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

start_date = pd.Timestamp(2015, 7, 1, 0)

fights = pd.read_json('../ETL/fights.json')
fights = fights.dropna()
fights = fights.reset_index(drop=True)

pre_USADA = fights[fights['date'] < start_date]
post_USADA = fights[fights['date'] >= start_date]

pre_missed = pre_USADA[pre_USADA['missed_weight'] == True].shape[0]
pre_made = pre_USADA[pre_USADA['missed_weight'] == False].shape[0]
post_missed = post_USADA[post_USADA['missed_weight'] == True].shape[0]
post_made = post_USADA[post_USADA['missed_weight'] == False].shape[0]

contingency = [[pre_missed, pre_made], [post_missed, post_made]]
chi2, p, dof, expected = stats.chi2_contingency(contingency)
print("Probability that fighters missed weight pre & post USADA is the same: " + str(round(p,4)) + "\n")
print("Expected: \n")
print(expected)
print("\n")
print("Contingency matrix: \n")
print(contingency)
