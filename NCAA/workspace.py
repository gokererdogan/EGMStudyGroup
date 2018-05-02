import numpy as np
import pandas as pd


def get_daynum(events_df, team1, team2):
    days1 = events_df[(events_df.WTeamID == team1) & (events_df.LTeamID == team2)].DayNum.unique()
    days2 = events_df[(events_df.WTeamID == team2) & (events_df.LTeamID == team1)].DayNum.unique()
    return np.concatenate((days1, days2))


def either_win_lose(events_df, team1, team2):
    days1 = events_df[(events_df.WTeamID == team1) & (events_df.LTeamID == team2)].DayNum.unique()
    days2 = events_df[(events_df.WTeamID == team2) & (events_df.LTeamID == team1)].DayNum.unique()
    return len(days1) > 0 and len(days2) > 0


def get_teams_stats(events_df):
    event_types = events['EventType'].unique()

    # Find Team statistics for each game
    match_stats_by_teams = events_df.groupby(['Season', 'DayNum', 'WTeamID', 'LTeamID', 'EventTeamID', 'EventType']) \
        .agg({'EventTeamID': 'count'}).rename(columns={'EventTeamID': 'Team_stat'}) \
        .reset_index(level=['EventTeamID', 'EventType'], inplace=True)

    ## TO DO
    # Find number of matches each team plays

    # Sum stats of each team

    # Divide the sum of stats by the number of matches team played

    # Update return
    return {'eventTypes': event_types}


if __name__ == "__main__":
    events = pd.read_csv('data/Events_2010.csv')
    d = events.groupby(['Season', 'EventTeamID', 'EventPlayerID', 'EventType']).agg({'EventPlayerID': 'count'})
    days = events['DayNum'].unique()
    teams = events['EventTeamID'].unique()
    players = events['EventPlayerID'].unique()
    events_indexed_with_day_and_team = events.set_index(['DayNum', 'WTeamID'])
