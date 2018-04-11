import pandas as pd

if __name__ == "__main__":
	events = pd.read_csv('data/Events_2010.csv')
	d = events.groupby(['Season', 'EventTeamID', 'EventPlayerID', 'EventType']).agg({'EventType': 'count'})
	print(d.head())
	print('Hello World!') #Hadi bakalim bileklere kuvvet!
