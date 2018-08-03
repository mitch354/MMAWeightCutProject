import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

fights = pd.read_json('../ETL/fights.json')
fights = fights.dropna()
fights = fights.reset_index(drop=True)

# Partition the dataframe by fights where the weight was missed
missed_weight = fights[fights['missed_weight'] == True]
made_weight = fights[fights['missed_weight'] == False]

missed_weight['age'] = missed_weight['age'].apply(lambda x: round(x, 2))
made_weight['age'] = made_weight['age'].apply(lambda x: round(x, 2))


print("Pvalue 1: " + str(stats.normaltest(missed_weight['age'].values).pvalue) + "\n")
print("Pvalue 2: " + str(stats.normaltest(made_weight['age'].values).pvalue) + "\n")
print("Equal variance: " + str(stats.levene(missed_weight['age'].values, made_weight['age'].values).pvalue) + "\n")

plt.xlabel('Age (Years)')
plt.ylabel('Frequency')
plt.title("Made Weight Fighter's ages")
plt.grid(True)
plt.hist(made_weight['age'].values)
plt.show()

ttest = stats.ttest_ind(missed_weight['age'].values, made_weight['age'].values)
print(ttest.pvalue)

print("Average missed weight age: " + str(np.mean(missed_weight['age'].values)))
print("Average made weight age: " + str(np.mean(made_weight['age'].values)))
