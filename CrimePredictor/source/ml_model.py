# -*- coding: utf-8 -*-
"""FinalProject (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yxZQ5MtdsEtjdVio8DCZyDQrL6aH_ipL

# CSCI: 470 Final Project: 
## Predicting rates of violent crime given socio-economic data from communities in the United States
### Team H2Li: Heidi Hufford, Hannah Levy, and Lindsey Nield
---
**This code reads in the UCI Crime and Communities dataset (from a file stored on the computer) and does the following:**
-The final feed-forward neural network used by the website
## Read in Data
"""

# Commented out IPython magic to ensure Python compatibility.
#Set up code
import numpy as np
import pandas as pd

from pandas import Series, DataFrame
from sklearn.model_selection import train_test_split, GridSearchCV

#Read in raw data
#Must have "communites.csv" on local drive
#Data can be downloaded from (http://archive.ics.uci.edu/ml/datasets/communities+and+crime) and saved as a csv 

import os
from django.conf import settings

raw_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'communities.csv'))

"""## Data Preprocessing"""

#Replace '?' with NA values
raw_data = raw_data.replace('?', np.NaN)

#Find out more about our data
raw_data.describe(include="all")

#Check how many values in each column are null
raw_data.isna().sum()

#Remove fold column
raw_data = raw_data.drop(columns=["fold"])

#Remove the state, county, community, and community name columns
#Create dataframe of community statistics (1993 observations)
community_data = raw_data.copy()
community_data = community_data.drop(columns=["state", "county", "community", "communityname"])

community_data = community_data[[c for c in community_data if community_data[c].isnull().sum() < 1000]]
community_data.dropna(inplace=True)

"""### Continuous Targets"""

#Predict using poverty
#Create X and y datasets with limited data
limited_data = community_data[["PctPopUnderPov", "ViolentCrimesPerPop"]]
X_limited = limited_data.copy()
X_limited = X_limited.drop(['ViolentCrimesPerPop'], axis=1)
y_limited = limited_data['ViolentCrimesPerPop'].copy()

X_train_limited, X_test_limited, y_train_limited, y_test_limited = train_test_split(X_limited, y_limited, random_state=0, test_size=0.2)

#Set up data for model building
import tensorflow as tf

import tensorflow.keras as keras
import numpy as np
from tensorflow.keras.layers import Dense, Dropout

print(X_train_limited.shape)
print(y_train_limited.shape)
print(X_test_limited.shape)
print(y_test_limited.shape)

X_train_limited = np.asarray(X_train_limited)
y_train_limited = np.asarray(y_train_limited)
X_test_limited = np.asarray(X_test_limited)
y_test_limited = np.asarray(y_test_limited)

X_train_limited = tf.convert_to_tensor(X_train_limited, dtype=tf.float32)
y_train_limited  = tf.convert_to_tensor(y_train_limited, dtype=tf.float32)
X_test_limited = tf.convert_to_tensor(X_test_limited, dtype=tf.float32)
y_test_limited  = tf.convert_to_tensor(y_test_limited, dtype=tf.float32)

layers = [
    Dense(10, input_shape=(1,), activation = 'tanh'),
    Dropout(0.05),
    Dense((10), activation = 'tanh'),
    Dropout(0.05),
    Dense((10), activation = 'tanh'),
    Dropout(0.05),
    Dense((10), activation = 'tanh'),
    Dropout(0.05),
    Dense((10), activation = 'tanh'),
    Dropout(0.05),
    Dense((10), activation = 'tanh'),
    Dropout(0.05),
    Dense(1, activation = 'tanh')
]
model_community = keras.Sequential(layers)

model_community.compile(optimizer='adam', loss='mae', metrics=["mae", "mse"])
model_community.fit(X_train_limited, y_train_limited, epochs=500, verbose=0)
model_community.summary()
model_community.evaluate(X_test_limited, y_test_limited)

# Save this model for later use
model_community.save(os.path.join(settings.BASE_DIR, 'source\keras-crime.h5'))
