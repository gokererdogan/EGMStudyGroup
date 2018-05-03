import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def create_dataset(stats, matches):
    """
    Create dataset from team statistics and match results.
    In input, each row is the team stats of first team followed by team stats of second team.
    In output, each row is the result of the corresponding match, with 1 denoting first team win.

    :param stats: A dataframe of team statistics with total event counts for each team in each row.
    :param matches: A dataframe of match results with winning team and losing team ids for one match in each row.
    :return: x, y. Two numpy arrays of stats and match results.
    """
    num_matches = matches.shape[0]
    feats_per_team = stats.shape[1]

    # allocate space for x and y
    x = np.zeros((num_matches, feats_per_team * 2))
    y = np.zeros(num_matches)

    i = 0
    skipped = 0  # if we can't find a team in stats dataframe, we skip that match.
    for _, row in matches.iterrows():  # loop over matches
        wteam = row.WTeamID
        lteam = row.LTeamID
        try:
            wteam_stats = stats.loc[wteam].values
            lteam_stats = stats.loc[lteam].values
        except KeyError:
            print("Can't find either {} or {}. Skipping.".format(wteam, lteam))
            skipped += 1
            continue

        # pick a random order for winning/losing teams.
        if np.random.rand() > 0.5:
            x[i, 0:feats_per_team] = wteam_stats
            x[i, feats_per_team:] = lteam_stats
            y[i] = 1
        else:
            x[i, 0:feats_per_team] = lteam_stats
            x[i, feats_per_team:] = wteam_stats
            y[i] = 0
        i += 1

    # if we skipped some matches, x and y has extra empty rows. do not return these.
    x = x[0:(num_matches-skipped)]
    y = y[0:(num_matches-skipped)]
    return x, y


if __name__ == "__main__":
    stats_season = 2010
    predict_season = 2011

    # get stats for each team in 2010 season
    # events = pd.read_csv('data/Events_{}.csv'.format(stats_season))
    # team_stats = events.groupby(['EventTeamID', 'EventType']).agg({'EventType': 'count'})
    # team_stats = team_stats.unstack('EventType')
    # team_stats.fillna(0, inplace=True)

    # load precalculated stats from disk
    team_stats = pd.read_csv('data/TeamStats_2010.csv', index_col=0, header=[0, 1])

    # get match results for 2011 season
    season_results = pd.read_csv('data/RegularSeasonCompactResults.csv')
    season_results = season_results[season_results.Season == predict_season]

    ncaa_results = pd.read_csv('data/NCAATourneyCompactResults.csv')
    ncaa_results = ncaa_results[ncaa_results.Season == predict_season]

    # use season results as training set and ncaa results as test set
    # form train/test datasets from stats and matches
    train_x, train_y = create_dataset(team_stats, season_results)
    test_x, test_y = create_dataset(team_stats, season_results)

    # Fit logistic regression and test accuracy on test dataset
    clf = LogisticRegression()
    clf.fit(train_x, train_y)
    test_acc = clf.score(test_x, test_y)
    print("Test accuracy: {}".format(test_acc))
