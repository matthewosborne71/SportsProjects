import pandas as pd

# Load in the data we pulled with GrabTeamData.py
shots = pd.read_csv(path + "NBAShots_2013_2019.csv")

# Add a ZONE_DETAIL variable
shots['ZONE_DETAIL'] = shots[['SHOT_ZONE_BASIC','SHOT_ZONE_AREA']].apply(lambda x: ','.join(x), axis = 1)
# Combine both Backcourt zones into one
shots.loc[shots.ZONE_DETAIL == 'Backcourt,Back Court(BC)','ZONE_DETAIL'] = 'Backcourt'
shots.loc[shots.ZONE_DETAIL == 'Above the Break 3,Back Court(BC)','ZONE_DETAIL'] = 'Backcourt'
shots = shots[['PLAYER_NAME','Season','ZONE_DETAIL','SHOT_MADE_FLAG']]

# Make Dummies
dummies = pd.get_dummies(shots['ZONE_DETAIL'])

# # Helps us know which zone is coded as ZONE_i, i = 0,...,15
zone_key = {}

# Helps with aesthetic so that zones are arranged in numerical order
def sort_key(x):
    if len(x) == 6:
        return int(x[5])
    else:
        return int(x[5:])

# Renaming the dummies with the numerical qualifiers we've created
i = 0
for col in dummies.columns:
    zone_key[col] = 'ZONE_' + str(i)
    i = i + 1

dummies = dummies.rename(columns = zone_key)
columns = list(dummies.columns)
columns.sort(key = sort_key)

# Add the dummies to shots df
for col in columns:
    shots[col] = dummies[col]


# Now that we've added the dummy variables we'll break our dataframe apart by
# season and save shot records for each season.


# We'll calculate how many shots we want each player to have shot
# This can be adjusted
# Say we want an average of 5 shots per game, and the player played 60 games
avg_shots_per_game = 5
game_num = 60
cutoff = avg_shots_per_game * game_num

# Gather the Seasons
seasons = list(set(shots.Season.values))
seasons.sort()

# We'll make a csv for each season
for season in seasons:
    season_shots = shots.loc[shots.Season == season,]

    # create a list of player names that beat the cutoff
    cutoff_names_T = season_shots.PLAYER_NAME.value_counts() > cutoff
    cutoff_names = cutoff_names_T[cutoff_names_T.values].index

    # Replace the dataframe with the one only including cutoff players
    elligible_index = season_shots[season_shots.isin(cutoff_names).values].index
    season_shots = season_shots.loc[elligible_index,]

    columns_wanted = []

    # How many total shots taken by each playet
    player_shots_by_zone = season_shots.groupby(['PLAYER_NAME']).size().to_frame('TOTAL_SHOTS')

    for col in columns:
        # How many shots in each zone
        player_shots_by_zone[col + '_ATT'] = season_shots.groupby(['PLAYER_NAME']).sum()[col]
        # How many made in each zone
        player_shots_by_zone[col + '_MADE'] = season_shots.loc[season_shots[col] == 1,].groupby(['PLAYER_NAME']).sum()['SHOT_MADE_FLAG']

        # Percent of shots taken that where in that zone
        player_shots_by_zone[col + '_PERC_OF_TOTAL_SHOTS'] = player_shots_by_zone[col + '_ATT']/player_shots_by_zone['TOTAL_SHOTS']
        # Percent of shots made in that zones
        player_shots_by_zone[col + '_PERC_MADE'] = player_shots_by_zone[col + '_MADE']/player_shots_by_zone[col + '_ATT']

        # What columns do we want
        columns_wanted.extend([col + '_PERC_OF_TOTAL_SHOTS', col + '_PERC_MADE'])

    player_shots_by_zone = player_shots_by_zone[columns_wanted]
    player_shots_by_zone.to_csv(path + "player_shots_by_zone_" + season + ".csv")

    player_shots_by_zone = None
    season_shots = None
    columns_wanted = None
    cutoff_names_T = None
    cutoff_names = None
    elligible_index = None
