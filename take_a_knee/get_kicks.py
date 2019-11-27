### get_kicks.py
### Written by: Matthew Osborne

### This code will scrape pro-football focus for all kickoff data

# Import the packages we'll need
from bs4 import BeautifulSoup
from bs4 import Comment
from urllib.request import urlopen

import pandas as pd
import numpy as np
import Path

path = Path.get_path()

######### Helper Functions ###############################

## This function reads in team and yard from the position column
## and returns the team and yard_line
def kick_team_and_yard(yard):
    if yard:
        team = yard.split(" ")[0]
        yard_line = 100 - int(yard.split(" ")[1])
    else:
        team = "error"
        yard_line = -99
    return team, yard_line

## two helper functions for grabbing team abbreviations
def clean_team_name(html):
    return html.split("/")[2]

def clean_name(name):
    name = name.replace("*","")
    name = name.replace("+","")
    return name

# this function takes in a season and returns a
# team abbreviation dictionary
def make_team_abbr_dict(year):
    # Read in the year page and make soup
    url = urlopen("https://www.pro-football-reference.com/years/" + str(year) + "/")
    soup = BeautifulSoup(url,"html.parser")

    # make the dict
    team_names = dict()

    # for the NFC
    for th in soup.find(id = "NFC").find_all("th"):
        if (th['data-stat'] == "team") & (th['scope'] == "row"):
            team_names[clean_name(th.text)] = clean_team_name(th.a['href']).upper()


    # for the AFC
    for th in soup.find(id = "AFC").find_all("th"):
        if (th['data-stat'] == "team") & (th['scope'] == "row"):
            team_names[clean_name(th.text)] = clean_team_name(th.a['href']).upper()

    return team_names

# this produces a dataframe containing the kickoffs and following plays
# given the profootball focus url for the game
def get_kicks(site,touchback_search,touchback_yard):
    # Open the website
    url = urlopen(site)

    # turn it to soup
    soup = BeautifulSoup(url,"html.parser")

    # the pbp table is stored in the comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # find the table
    for i in range(len(comments)):
        if "Play-By-Play" in comments[i]:
            pbp = i

    # make the table parsable
    pbp_table = BeautifulSoup(comments[pbp],"html.parser")

    # Now we make a df to hold all the plays from the game
    plays = {'quarter':[],'time_left':[],'position':[],'description':[]}

    for tr in pbp_table.find("tbody").find_all("tr"):
        if len(tr.find_all("th")) > 0:
            if tr.find("th",{'data-stat':'quarter'}).text != "Quarter":
                plays['quarter'].append(tr.find("th",{'data-stat':'quarter'}).text)
        for td in tr.find_all("td"):
            if td['data-stat'] == 'qtr_time_remain':
                plays['time_left'].append(td.text)
            elif td['data-stat'] == 'location':
                plays['position'].append(td.text)
            elif td['data-stat'] == 'detail':
                plays['description'].append(td.text)


    plays = pd.DataFrame(plays)

    # Grab the kick offs (excluding onside)
    # and following plays
    indices = []
    for i in plays.loc[plays.description.str.contains("kicks off"),].index:
        if "no play" not in plays.description[i]:
            if i+1 in plays.index:
                indices.extend([i,i+1])
                if i + 2 in plays.index:
                    indices.extend([i+2])
            else:
                indices.append(i)

        if touchback_search & ("touchback" in plays.description[i]):
            touchback_search = False
            touchback_yard = int(plays.position[i+1].split(" ")[1])


    kicks = plays.loc[indices,].copy()
    kicks['last_play'] = False

    kicks = kicks.drop_duplicates()

    for i in kicks.index:
        if "kicks off" in kicks.description[i].lower():

            if (i+1 not in plays.index):
                kicks.loc[i,'last_play'] = True
            elif ('2' == plays.loc[i,'quarter']) & ('2' != plays.loc[i+1,'quarter']):
                kicks.loc[i,'last_play'] = True


    return kicks,touchback_search,touchback_yard

# This function reads in a kick description and finds
# how far the kick was, if it resulted in a touchback,
# and if a penalty occurred.
# This function reads in a kick description and finds
# how far the kick was, if it resulted in a touchback,
# and if a penalty occurred.
def analyze_kick(kick,empty,last_play):
    return_length = "None"
    if "gain" == kick.lower().split(",")[0].split(" yard")[0].split(" ")[-1]:
        kick_length = np.nan
    else:
        kick_length = int(kick.lower().split(",")[0].split(" yard")[0].split(" ")[-1])
    touchback = "touchback" in kick.lower()
    penalty = "penalty" in kick.lower()
    turnover = "fumble" in kick.lower()
    touchdown = "touchdown" in kick.lower()


    if last_play:
        if "return" not in kick:
            return_length = 0
        else:
            return_length = kick.split(" yard")[1].split(" ")[-1]
        return kick_length,touchback,penalty,turnover,touchdown,return_length
    else:
        return kick_length,touchback,penalty,turnover,touchdown,return_length

## This function returns the relative position a kick was returned to,
## relative to the return team
def returned_to(item, return_team):
    if item:
        if item.split(" ")[0] == return_team:
            return int(item.split(" ")[1])
        else:
            return 100 - int(item.split(" ")[1])
    else:
        return -99

# This function will take in the kicks df and produce a dictionary
# that breaks down each kick from that game
# This function will take in the kicks df and produce a dictionary
# that breaks down each kick from that game
# This function will take in the kicks df and produce a dictionary
# that breaks down each kick from that game
def get_game_dict(kicks,team_1,team_2,tb_y):
    # holder for this game's kick info
    game_dict = {"kick_team":[],"return_team":[],"kicked_from":[],"kick_length":[],
                     "returned_to":[],"touchback":[],"penalty":[],"turnover":[],"touchdown":[],"last_play":[]}

    # for each kick event
    for i in kicks.index:
        if "kicks off" in kicks.description[i]:
            # was the kick the last play of the game?
            empty = not (i+1 in kicks.index)

            # extract the relevant info from the kick
            t_and_y,kick_info = kick_team_and_yard(kicks.position[i]), analyze_kick(kicks.description[i],empty,kicks.last_play[i])

            # add the kicking team
            try:
                if t_and_y[0] == "error":
                    return_team = kick_team_and_yard(kicks.position[i+1])
                    if return_team == team_1:
                        game_dict['kick_team'].append(team_2)
                        kick_team = team_2
                    else:
                        game_dict['kick_team'].append(team_1)
                        kick_team = team_1
                else:

                    game_dict['kick_team'].append(t_and_y[0])
                    kick_team = t_and_y[0]


                    # add the return team
                if kick_team == team_1:
                    return_team = team_2
                    game_dict['return_team'].append(team_2)
                else:
                    return_team = team_1
                    game_dict['return_team'].append(team_1)
            except:
                game_dict['kick_team'].append(np.nan)
                game_dict['return_team'].append(np.nan)




            # add the kicked from, note relative to return team ez
            game_dict['kicked_from'].append(t_and_y[1])

            # Get length of kick
            game_dict['kick_length'].append(kick_info[0])

            # Was it a touchback?
            game_dict['touchback'].append(kick_info[1])

            # Was there a penalty?
            game_dict['penalty'].append(kick_info[2])

            # Was there a turnover?
            game_dict['turnover'].append(kick_info[3])

            # Was it returned for a td?
            game_dict['touchdown'].append(kick_info[4])

            # Was it the last play of a half?
            game_dict['last_play'].append(kicks.last_play[i])

            # Where was it returned to?
            # Was there a turnover on the return?
            if kick_info[3]:
                game_dict['returned_to'].append(np.nan)
            # check for touchback, and no penalty
            elif (kick_info[1]) & (not kick_info[2]):
                game_dict['returned_to'].append(tb_y)
            # Was it returned for a td?
            elif (kick_info[4]):
                game_dict['returned_to'].append(100)
            # Was it the last play of a half?
            elif (kicks.last_play[i]):
                if "None" != kick_info[5]:
                    game_dict['returned_to'].append(int(t_and_y[1]) - int(kick_info[0]))
                else:
                    game_dict['returned_to'].append(int(t_and_y[1]) - int(kick_info[0]) + int(kick_info[5]))
            else:
                if returned_to(kicks.loc[i+1,'position'],return_team) == -99:
                    game_dict['returned_to'].append(returned_to(kicks.loc[i+2,'position'],return_team))
                else:
                    game_dict['returned_to'].append(returned_to(kicks.loc[i+1,'position'],return_team))
    return game_dict

##### End of helper functions #############

##### Script ##############################

# The seasons we want
seasons = range(2005,2020,1)

for year in seasons:
    # Get the team abbreviations for that season
    teams = make_team_abbr_dict(year)

    # Get the soup for this particular season
    url = urlopen("https://www.pro-football-reference.com/years/" +
                    str(year) + "/games.htm")
    soup = BeautifulSoup(url, "html.parser")
    table = soup.find(id = 'games')

    # This will hold the data from each game
    season_dict = {'week':[],'game_dicts':[]}

    # Until we know what the touchback yardage is for this season
    # We will need to search for it
    touchback_search = True
    tb_y = 0

    # for each game in the season we will find the kick data from that game
    for tr in table.find("tbody").find_all("tr"):
        if ("Week" not in tr.find("th",{"data-stat":"week_num"}).text):
            if "boxscore" in tr.find("td",{"data-stat":"boxscore_word"}).text:
                print("Still getting games from " + str(year) + " week " + tr.find("th",{"data-stat":"week_num"}).text)
                # week of the game
                season_dict['week'].append(tr.find("th",{"data-stat":"week_num"}).text)

                # team_1 in the game
                team_1 = teams[tr.find("td",{"data-stat":"winner"}).text]
                # team_2 in the game
                team_2 = teams[tr.find("td",{"data-stat":"loser"}).text]
                # url for the game
                game_url = "https://www.pro-football-reference.com" + tr.find("td",{"data-stat":"boxscore_word"}).a['href']

                kicks,touchback_search,tb_y = get_kicks(game_url,touchback_search,tb_y)
                season_dict['game_dicts'].append(get_game_dict(kicks,team_1,team_2,tb_y))

    all_games = []
    for i in range(len(season_dict['week'])):
        temp_df = pd.DataFrame(season_dict['game_dicts'][i])
        temp_df['week'] = season_dict['week'][i]
        all_games.append(temp_df)

    season_df = pd.concat(all_games,ignore_index = True)

    season_df.to_csv(path + str(year) + "_kicks.csv",index = False)
