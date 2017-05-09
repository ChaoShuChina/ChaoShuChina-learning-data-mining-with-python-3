__author__ = 'chao-shu'
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

standingfilename = "2012-2013standing.csv"
standings = pd.read_csv(standingfilename)
# print(standings)
dataset['HomeTeamRanksHigher'] = 0
for index, row in dataset.iterrows():
    HomeTeam = row['HomeTeam']
    VisitorTeam = row['VisitorTeam']
    if HomeTeam == "New Orleans Pelicans":
        HomeTeam = "New Orleans Hornets"
    elif VisitorTeam == "New Orleans Pelicans":
        VisitorTeam = "New Orleans Hornets"
    HomeRank = standings[standings["Team"] == HomeTeam]['Rk'].values[0]
    VistitorRank = standings[standings['Team'] == VisitorTeam]['Rk'].values[0]
    row['HomeTeamRanksHigher'] = int(HomeRank < VistitorRank)
    dataset.ix[index] = row

XhomeHigher = dataset[["HomeLastWin", "VisitorLastWin", "HomeTeamRanksHigher"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, XhomeHigher, y_true)
out = np.mean(scores) * 100
print(out)