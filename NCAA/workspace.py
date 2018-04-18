import numpy as np
import pandas as pd


def get_daynum(events, team1, team2):
	days1 = events[(events.WTeamID == team1) & (events.LTeamID == team2)].DayNum.unique()
	days2 = events[(events.WTeamID == team2) & (events.LTeamID == team1)].DayNum.unique()
	return np.concatenate((days1, days2))


if __name__ == "__main__":
    events = pd.read_csv('data/Events_2010.csv')
    d = events.groupby(['Season', 'EventTeamID', 'EventPlayerID', 'EventType']).agg({'EventType': 'count'})
    print(d.head())
    print('Hello World!')  # Hadi bakalim bileklere kuvvet!
