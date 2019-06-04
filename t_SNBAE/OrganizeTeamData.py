import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import Path

path = Path.get_path()

# Load in the data we pulled with GrabTeamData.py
TeamShots = pd.read_csv(path + "NBAShots_2013_2019.csv")

# Add a new variable that combines the two shot zone variables into one
TeamShots['ZONE_DETAIL'] = TeamShots[['SHOT_ZONE_BASIC','SHOT_ZONE_AREA']].apply(lambda x: '-'.join(x).replace(" ", "_"), axis = 1)
# Combine both Backcourt zones into one
TeamShots.loc[TeamShots.ZONE_DETAIL == 'Backcourt-Back_Court(BC)','ZONE_DETAIL'] = 'Backcourt'
TeamShots.loc[TeamShots.ZONE_DETAIL == 'Above_the_Break_3-Back_Court(BC)','ZONE_DETAIL'] = 'Backcourt'


# This will plot and save a picture of all the zones created in ZONE_DETAIL.
# The plot will make it easier to visualize where all of the ZONE_DETAIL zones
# are on the court

# get the colors to paint each zone
cm = plt.get_cmap('tab20')
n_zones = len(set(TeamShots.ZONE_DETAIL.values))
colors = [cm(i) for i in range(n_zones)]

# plot the x-y coordinates of each shot and color by ZONE_DETAIL
sns.lmplot(data = TeamShots, x = 'LOC_X', y = 'LOC_Y', hue = 'ZONE_DETAIL',
            palette = colors, fit_reg = False, scatter_kws = {'s':5})
plt.savefig("ZONE_DETAIL_Court_Location.png")
plt.close()

# Isolate just the team, season, ZONE_DETAIL, and make/miss
Shot_by_Zone = TeamShots[['TEAM_NAME','Season','ZONE_DETAIL','SHOT_MADE_FLAG']].copy()

# Create Dummy Variables
Dummies = pd.get_dummies(Shot_by_Zone['ZONE_DETAIL'])



# These will be used to get our columns later
Columns = list(Dummies.columns)

# Add dummy variables to our dataframe
for col in Columns:
    Shot_by_Zone[col] = Dummies[col]

del Dummies

Columns_Wanted = []

# How many total shots were taken by each team in each season
SHOTS_BY_ZONE = Shot_by_Zone.groupby(['TEAM_NAME','Season']).size().to_frame('TOTAL_SHOTS')

# For each of the zones
for col in Columns:
    # How many shots were attempted in that zone for each team in each season
    SHOTS_BY_ZONE[col + '_ATT'] = Shot_by_Zone.groupby(['TEAM_NAME','Season']).sum()[col]
    # How many shots were made in that zone for each team in each season
    SHOTS_BY_ZONE[col + '_MADE'] = Shot_by_Zone.loc[Shot_by_Zone[col] == 1,].groupby(['TEAM_NAME','Season']).sum()['SHOT_MADE_FLAG']

    # Now calculate what percentage of a teams shots were in that zone
    SHOTS_BY_ZONE[col + '_PERC_TOT'] = SHOTS_BY_ZONE[col + '_ATT']/SHOTS_BY_ZONE['TOTAL_SHOTS']
    # Now calculate what percentage of shots taken in that zone were made
    SHOTS_BY_ZONE[col + '_PERC_MADE'] = SHOTS_BY_ZONE[col + '_MADE']/SHOTS_BY_ZONE[col + "_ATT"]

    # These are the columns we want in our final df
    Columns_Wanted.extend([col + '_PERC_TOT',col + '_PERC_MADE'])



# Save only the columns we want
SHOTS_BY_ZONE = SHOTS_BY_ZONE[Columns_Wanted].copy()

# Break down by 3, mid, and close range
col_3 = []
col_mid = []
col_close = []

for c in Columns_Wanted:
    if '_PERC_TOT' in c:
        if ('3' in c) or (c == 'Backcourt'):
            col_3.append(c)
        elif 'Mid' in c:
            col_mid.append(c)
        else:
            col_close.append(c)

SHOTS_BY_ZONE['3_PERC_OF_TOT'] = SHOTS_BY_ZONE[col_3].sum(axis = 1)
SHOTS_BY_ZONE['MID_PERC_OF_TOT'] = SHOTS_BY_ZONE[col_mid].sum(axis = 1)
SHOTS_BY_ZONE['CLOSE_PERC_OF_TOT'] = SHOTS_BY_ZONE[col_close].sum(axis = 1)



SHOTS_BY_ZONE.to_csv(path + "Team_Shots_by_Zone.csv")
