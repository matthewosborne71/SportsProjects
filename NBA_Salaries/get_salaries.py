## get_salaries.py
## Written by: Matthew Osborne
## Date 12-20-20
#################
## This script will give you the player salaries from the 1985-2021 NBA seasons
## by scraping basketball-reference using BeautifulSoup
##################

## import packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import Comment
import pandas as pd

# Set the start and end of the destination url for each season
start_url = "https://www.basketball-reference.com"

# read in the endpoints created by get_team_endpoints.py
endpoints = pd.read_csv("Data/team_endpoints.csv")

# create the data file
file = open("Data/salaries.csv","w+")
file.write("season,team,player,salary\n")

# for each endpoint
for i in endpoints.index:
    season = str(endpoints.season[i])
    team = endpoints.team[i]
    endpoint = endpoints.endpoint[i]

    print("Working on " + season + " " + team)

    # make the season-team soup
    url = start_url + endpoint
    html = urlopen(url)
    soup = BeautifulSoup(html,"html.parser")

    # find the salaries2 table
    for c in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if ("table" in c) and ("salaries2" in c):
            table = BeautifulSoup(c,"html.parser").table

    # write down the player name and salary
    for tr in table.find_all("tr")[1:]:
        player = tr.find('td',{'data-stat':"player"}).text.replace(",","")
        salary = tr.find('td',{'data-stat':"salary"}).text.replace(",","").strip("$")
        file.write(season + "," + team + "," + player + "," + salary + "\n")

# close the file
file.close()
