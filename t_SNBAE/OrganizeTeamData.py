import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load in the data we pulled with GrabTeamData.py
TeamShots = pd.read_csv("NBAShots_2013_2019.csv")

# Add a new variable that combines the two shot zone variables into one
TeamShots['ZONE_DETAIL'] = TeamShots[['SHOT_ZONE_BASIC','SHOT_ZONE_AREA']].apply(lambda x: ','.join(x), axis = 1)
# Combine both Backcourt zones into one
TeamShots.loc[TeamShots.ZONE_DETAIL == 'Backcourt,Back Court(BC)','ZONE_DETAIL'] = 'Backcourt'
TeamShots.loc[TeamShots.ZONE_DETAIL == 'Above the Break 3,Back Court(BC)','ZONE_DETAIL'] = 'Backcourt'

# This will plot and save a picture of all the zones created in ZONE_DETAIL.
# The plot will make it easier to visualize where all of the ZONE_DETAIL zones
# are on the court

# get the colors to paint each zone
cm = plt.get_cmap('tab20')
n_zones = len(set(TeamShots.ZONE_DETAIL.values))
colors = [cm(i) for i in range(n_zones)]

# plot the x-y coordinates of each shot and color by ZONE_DETAIL
sns.lmplot(data = TeamShots, x = 'LOC_X', y = 'LOC_Y', hue = 'ZONE_DETAIL',
            palette = colors, fit_reg = False, scatter_kws = {'s':2})
plt.savefig("ZONE_DETAIL_Court_Location.png")
plt.close()

# Isolate just the team, season, ZONE_DETAIL, and make/miss
Shot_by_Zone = TeamShots[['TEAM_NAME','Season','ZONE_DETAIL','SHOT_MADE_FLAG']]

# Create Dummy Variables
Dummies = pd.get_dummies(Shot_by_Zone['ZONE_DETAIL'])

# Helps us know which zone is coded as ZONE_i, i = 0,...,15
ZoneKey = {}
i = 0

# Helps with aesthetic so that zones are arranged in numerical order
def sort_key(x):
    if len(x) == 6:
        return int(x[5])
    else:
        return int(x[5:])


for col in Dummies.columns:
    ZoneKey[col] = 'ZONE_' + str(i)
    i = i + 1
del i

Dummies = Dummies.rename(columns = ZoneKey)

# These will be used to get our columns later
Columns = list(Dummies.columns)
Columns.sort(key = sort_key)

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
    SHOTS_BY_ZONE[col + '_PERC_OF_TOTAL_SHOTS'] = SHOTS_BY_ZONE[col + '_ATT']/SHOTS_BY_ZONE['TOTAL_SHOTS']
    # Now calculate what percentage of shots taken in that zone were made
    SHOTS_BY_ZONE[col + '_PERC_MADE'] = SHOTS_BY_ZONE[col + '_MADE']/SHOTS_BY_ZONE[col + "_ATT"]

    # These are the columns we want in our final df
    Columns_Wanted.extend([col + '_PERC_OF_TOTAL_SHOTS',col + '_PERC_MADE'])

# Record the zone key so we know what zones are coded as ZONE_i
f = open("ZONE_KEY.csv","w+")
f.write("ZONE_DETAIL,CODE\n")
for key in ZoneKey.keys():
    f.write(key + "," + ZoneKey[key] + "\n")

f.close()

# Save the df with the desired columns
SHOTS_BY_ZONE = SHOTS_BY_ZONE[Columns_Wanted]
SHOTS_BY_ZONE.to_csv("Team_Shots_by_Zone.csv")
