#### GrabTeamData.py
#### Written by: Matthew Osborne
#### Last updated 4 - 10 - 2019
######################################

# import the packages we will need #
# Data Handling
import pandas as pd

# nba scraper
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
import time

# Get the NBA teams
Teams = teams.get_teams()
TeamIDs = [team['id'] for team in Teams]

# We'll pull data on the last five seasons
Seasons = [str(year) + "-" + str(year + 1)[2:4] for year in range(2013,2019,1)]

# Data we'll want
Columns = ['TEAM_ID','TEAM_NAME','GAME_ID','GAME_DATE','PLAYER_ID','PLAYER_NAME',
            'PERIOD','MINUTES_REMAINING','SECONDS_REMAINING','ACTION_TYPE','SHOT_TYPE',
            'SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE',
            'LOC_X','LOC_Y','SHOT_MADE_FLAG','HTM','VTM']

First = True

# For each season
for Season in Seasons:
    # For each team
    for ID in TeamIDs:
        # We'll grab the shot chart data for the team, extract the relevant
        # columns from the dataframe, then append the most recently retrieved
        # data onto the running dataframe.
        if First:
            First = False
            NBAShots_DF = shotchartdetail.ShotChartDetail(team_id = ID,
                            player_id = 0,
                            season_nullable = Season,
                            context_measure_simple = 'FGA').get_data_frames()[1][Columns]
            NBAShots_DF['Season'] = Season
        else:
            Temp_DF = shotchartdetail.ShotChartDetail(team_id = ID,
                            player_id = 0,
                            season_nullable = Season,
                            context_measure_simple = 'FGA').get_data_frames()[1][Columns]
            Temp_DF['Season'] = Season
            NBAShots_DF = pd.concat([NBAShots_DF,Temp_DF])
            del Temp_DF

        # To help us keep track of progress, the rest is to make sure we
        # aren't scraping too quickly
        print("Resting 5 seconds.")
        time.sleep(5)
    print("Finished for " + str(Season) + " season.")

# Write the data to file 
NBAShots_DF.to_csv("NBAShots_2013_2019.csv", index = False)