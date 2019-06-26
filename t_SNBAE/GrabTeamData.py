#### GrabTeamData.py
#### Written by: Matthew Osborne
#### Last updated 4 - 10 - 2019
######################################

# import the packages we will need #
# Data Handling
import pandas as pd
import Path

# nba scraper
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartdetail
import time

# Get the path
path = Path.get_path()

# Get the NBA teams
Teams = teams.get_teams()
TeamIDs = [team['id'] for team in Teams]
print([team['full_name'] for team in Teams])

# We'll pull data on since 2000
Seasons = [str(year) + "-" + str(year + 1)[2:4] for year in range(2000,2019,1)]

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
            NBAShots = shotchartdetail.ShotChartDetail(team_id = ID,
                            player_id = 0,
                            season_nullable = Season,
                            context_measure_simple = 'FGA')
            if len(NBAShots.get_data_frames()[0]) != 0:
                NBAShots_DF = [df for df in NBAShots.get_data_frames() if df['GRID_TYPE'][0] == 'Shot Chart Detail'][0][Columns].copy()
                NBAShots_DF['Season'] = Season
                del NBAShots
            else:
                First = True
        else:
            Temp = shotchartdetail.ShotChartDetail(team_id = ID,
                            player_id = 0,
                            season_nullable = Season,
                            context_measure_simple = 'FGA')
            if len(Temp.get_data_frames()[0]) != 0:
                Temp_DF = [df for df in Temp.get_data_frames() if df['GRID_TYPE'][0] == 'Shot Chart Detail'][0][Columns].copy()
                Temp_DF['Season'] = Season
                NBAShots_DF = pd.concat([NBAShots_DF,Temp_DF])
                del Temp_DF
                del Temp

        # To help us keep track of progress, the rest is to make sure we
        # aren't scraping too quickly
        print("Resting 5 seconds.")
        #time.sleep(5)
    print("Finished for " + str(Season) + " season.")

# Write the data to file
# Note this is a largish csv file
NBAShots_DF.to_csv(path + "NBAShots_2000_2019.csv", index = False)
