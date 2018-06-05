import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss


def create_dataset_from_years(years, num_best_players):
    xs = []
    ys = []
    ncaa_results = pd.read_csv('data/NCAATourneyCompactResults.csv')

    for year in years:
        # create player stats
        player_stats, best_players = create_best_player_stats(year, num_best_players)

        # read matches
        ncaa_year_results = ncaa_results[ncaa_results.Season == year]
        x, y = create_dataset(player_stats, ncaa_year_results, best_players, num_best_players)
        xs.append(x)
        ys.append(y)

    return np.concatenate(xs, axis=0), np.concatenate(ys, axis=0)


def create_dataset(player_stats, matches, best_players, num_best_players=11):
    """
    Create dataset from player statistics and match results.

    :param player_stats: A dataframe of player statistics with total event counts for each player in each row.
    :param matches: A dataframe of match results with winning team and losing team ids for one match in each row.
    :param best_players: A dataframe of best 11 players for each team.
    :param num_best_players: Number of players per team.
    :return: x, y. Two numpy arrays of stats and match results.
        x is number of matches x 2 teams x number of players x number of events.
        y is a vector  of length number of matches of match results (0-1).
    """
    num_matches = matches.shape[0]
    feats_per_team = player_stats.shape[1]

    # allocate space for x and y
    x = np.zeros((num_matches, feats_per_team * num_best_players * 2))
    y = np.zeros(num_matches)

    i = 0
    for _, row in matches.iterrows():  # loop over matches
        wteam = row.WTeamID
        lteam = row.LTeamID

        wteam_stats = getBestPlayerStats(best_players, player_stats, wteam).flatten()
        lteam_stats = getBestPlayerStats(best_players, player_stats, lteam).flatten()

        # pick a random order for winning/losing teams.
        if np.random.rand() > 0.5:
            x[i, 0:(num_best_players*feats_per_team)] = wteam_stats
            x[i, (num_best_players*feats_per_team):] = lteam_stats
            y[i] = 1
        else:
            x[i, 0:(num_best_players*feats_per_team)] = lteam_stats
            x[i, (num_best_players*feats_per_team):] = wteam_stats
            y[i] = 0
        i += 1

    return x, y


def getBestPlayerStats(bestPlayersDf, player_stats_df, TeamID):
    players = list(bestPlayersDf[bestPlayersDf['EventTeamID'] == TeamID]['EventPlayerID'])
    return player_stats_df.loc[players].values


def create_best_player_stats(year, num_best_players):
    events = pd.read_csv("data/Events_{}.csv".format(year))

    # get statistics for each player
    season_events = events[events.DayNum < 134]
    g = season_events.groupby(['EventPlayerID', 'EventType']).agg({'EventType': 'count'})
    player_stats = g.unstack(['EventType'], fill_value=0)

    best_players = season_events.groupby(['EventTeamID', 'EventPlayerID']).agg({'EventType': 'count'}) \
        .reset_index().groupby(['EventTeamID']).apply(lambda x: x.nlargest(num_best_players, 'EventType'))

    return player_stats, best_players


if __name__ == "__main__":
    # season matches are daynum < 134
    # ncaa matches are daynum >= 134 (64-67 games)
    # events data contain extra matches that are not part of NCAA

    train_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
    test_years = [2017]

    num_best_players = 5
    train_x, train_y = create_dataset_from_years(train_years, num_best_players)
    test_x, test_y = create_dataset_from_years(test_years, num_best_players)

    clf = LogisticRegression()
    clf.fit(train_x, train_y)
    print("Train accuracy: ", clf.score(train_x, train_y))

    print("Test accuracy: ", clf.score(test_x, test_y))
    print("Test log loss: ", log_loss(test_y, clf.predict_proba(test_x)))


