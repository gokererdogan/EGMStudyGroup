import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


def create_game_stats(events):

    # Day number, winning team id and losing team id uniquely determines the game id
    col = events['DayNum'].astype(str) + "_" + events['WTeamID'].astype(str) + "_" + events['LTeamID'].astype(str)
    events['GameID'] = col
    # new column indicating the winning team
    events.EventTeamID = (events.WTeamID == events.EventTeamID)
    events.EventTeamID = events.EventTeamID.astype(int)

    g = events.groupby(['GameID', 'EventTeamID', 'EventType']).agg({'EventType': 'count'})
    us = g.unstack(['EventTeamID', 'EventType'], fill_value=0)

    return us.sort_index(axis=1)


if __name__ == "__main__":

    events_2010 = pd.read_csv("data/Events_2010.csv")

    nus = create_game_stats(events_2010)

    x = nus.values
    flip_i = np.random.rand(x.shape[0]) > 0.5
    x[flip_i] = np.concatenate((x[flip_i, 25:], x[flip_i, 0:25]), axis=1)


    x = np.nan_to_num(x)

    y = np.zeros(x.shape[0])
    y[flip_i] = 1

    clf = LogisticRegression()
    clf.fit(x, y)
    clf.score(x, y)

    c = clf.coef_.T

    print(np.max(c))
    print(np.argmax(c))

    print(nus.iloc[0])
