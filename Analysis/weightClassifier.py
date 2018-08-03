import pandas as pd
import datetime
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

todayStamp = datetime.datetime.now()

def getAge(dob):
    age = (todayStamp - dob).days
    age = age / 365.25
    return age

fighters = pd.read_json('../ETL/fighters.json')
fighters = fighters[~fighters['weight_class'].str.contains("Women's")]
fighters['dob'] = pd.to_datetime(fighters['dob'])
fighters['age'] = fighters['dob'].apply(getAge)
fighters = fighters.dropna()
fighters = fighters.reset_index()

model = make_pipeline(
    StandardScaler(),
    GaussianNB()
    #SVC(kernel='linear', C=10)
    #KNeighborsClassifier(n_neighbors=5)
)

X = fighters[['height', 'reach', 'age']].values
y = fighters['weight_class'].values
X_train, X_test, y_train, y_test = train_test_split(X, y)
model.fit(X_train, y_train)
print("Accuracy: " + str(round(model.score(X_test, y_test), 3)))
