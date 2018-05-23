import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


def create_dataset(player_stats, matches):
    """
    Create dataset from player statistics and match results.

    :param player_stats: A dataframe of player statistics with total event counts for each player in each row.
    :param matches: A dataframe of match results with winning team and losing team ids for one match in each row.
    :return: x, y. Two numpy arrays of stats and match results.
        x is number of matches x 2 teams x number of players x number of events.
        y is a vector  of length number of matches of match results (0-1).
    """
    pass


if __name__ == "__main__":
    # season matches are daynum < 134
    # ncaa matches are daynum >= 134 (64-67 games)
    # events data contain extra matches that are not part of NCAA

    events_2010 = pd.read_csv("data/Events_2010.csv")

    # get statistics for each player
    season_events = events_2010[events_2010.DayNum < 134]
    g = season_events.groupby(['EventPlayerID', 'EventType']).agg({'EventType': 'count'})
    player_stats = g.unstack(['EventType'], fill_value=0)

