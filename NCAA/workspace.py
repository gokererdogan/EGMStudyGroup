import numpy as np
import pandas as pd


def get_daynum(events, team1, team2):
    days1 = events[(events.WTeamID == team1) & (events.LTeamID == team2)].DayNum.unique()
    days2 = events[(events.WTeamID == team2) & (events.LTeamID == team1)].DayNum.unique()
    return np.concatenate((days1, days2))


def either_win_lose(events, team1, team2):
    days1 = events[(events.WTeamID == team1) & (events.LTeamID == team2)].DayNum.unique()
    days2 = events[(events.WTeamID == team2) & (events.LTeamID == team1)].DayNum.unique()
    return len(days1) > 0 and len(days2) > 0


if __name__ == "__main__":
    events = pd.read_csv('data/Events_2010.csv')
    d = events.groupby(['Season', 'EventTeamID', 'EventPlayerID', 'EventType']).agg({'EventPlayerID': 'count'})
    days = events['DayNum'].unique()
    teams =events['EventTeamID'].unique()
    players = events['EventPlayerID'].unique()
    events_indexed_with_day_and_team = events.set_index(['DayNum', 'WTeamID'])

    events['GameID'] = events['DayNum'] * 10000 + events['WTeamID']
    df = pd.DataFrame(events[['EventID', 'EventTeamID', 'ElapsedSeconds', 'EventPlayerID', 'EventType', 'GameID']]).set_index('GameID')
    df = df.groupby(['GameID', 'EventTeamID', 'EventType']).agg({'EventType': 'count'})
    df = df.unstack('EventType', fill_value=0)
    df = df.groupby(['GameID']).apply(lambda x: pd.concat([x.iloc[0], x.iloc[1]]))
