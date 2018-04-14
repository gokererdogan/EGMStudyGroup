import pandas as pd

if __name__ == "__main__":
    events = pd.read_csv('data/Events_2010.csv')
    d = events.groupby(['Season', 'EventTeamID', 'EventPlayerID', 'EventType']).agg({'EventPlayerID': 'count'})
    days = events['DayNum'].unique()
    teams =events['EventTeamID'].unique()
    players = events['EventPlayerID'].unique()
    events_indexed_with_day_and_team = events.set_index(['DayNum', 'WTeamID'])
