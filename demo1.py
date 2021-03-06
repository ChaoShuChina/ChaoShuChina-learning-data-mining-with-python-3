import pandas as pd
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
import numpy as np

dataset = pd.read_csv('2013-2014_Games.csv', parse_dates=['Date'])
dataset.columns = ['Date', 'StartTime', 'VisitorTeam', 'VisitorPts', 'HomeTeam', 'HomePts', 'OT?']
dataset['HomeWin'] = dataset['VisitorPts'] < dataset['HomePts']
dataset['HomeLastWin'] = False
dataset['VisitorLastWin'] = False

y_true = dataset['HomeWin'].values

won_last = defaultdict(int)
for index, row in dataset.sort('Date').iterrows():
    HomeTeam = row['HomeTeam']
    VisitorTeam = row['VisitorTeam']
    row['HomeLastWin'] = won_last[HomeTeam]
    row['VisitorLastWin'] = won_last[VisitorTeam]
    dataset.ix[index] = row
    won_last[HomeTeam] = row['HomeWin']
    won_last[VisitorTeam] = not row['HomeWin']

# print(dataset.ix[20:25])
clf = DecisionTreeClassifier(random_state=14)
x_previouswins = dataset[['HomeLastWin', 'VisitorLastWin']].values

scores = cross_val_score(clf, x_previouswins, y_true)
out = np.mean(scores) * 100
print out
