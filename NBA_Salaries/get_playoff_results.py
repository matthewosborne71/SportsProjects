## get_playoff_results.py
## Written by: Matthew Osborne
## Date 12-20-20
#################
## This script will give you the playoff results from the 1985-2020 NBA seasons
## by scraping basketball-reference using BeautifulSoup
##################

## import the packages needed
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import Comment
import pandas as pd

# set the url start and end for each season
url_start = "https://www.basketball-reference.com/playoffs/NBA_"
url_end = ".html"

# open the file that will hold the data
file = open("Data/playoffs.csv","w+")
file.write("season,team,outcome\n")

# for each season from 1985-2020
for season in range(1985,2021):
    print("Working on season",str(season))
    # make the soup for that season
    url = url_start + str(season) + url_end
    html = urlopen(url)
    soup = BeautifulSoup(html,"html.parser")

    table = soup.find("table",{'id':"all_playoffs"})

    outcome_dict = {}

    # Find the playoff results for that season
    for tr in table.find_all("tr"):
        if ("Finals" in str(tr)) or ("Conference" in str(tr)):
            tds = tr.find_all("td")
            round = tds[0].text.replace("Western ","").replace("Eastern ","")
            if "First Round" in round:
                round = "First Round"
            winner = tds[1].find_all("a")[0].text
            loser = tds[1].find_all("a")[1].text
            if winner not in outcome_dict.keys():
                outcome_dict[winner] = "Larry O'Brien Winner"
            outcome_dict[loser] = round

    # write the data to file
    for team,outcome in zip(list(outcome_dict.keys()),list(outcome_dict.values())):
        file.write(str(season) + "," + team + "," + outcome + "\n")

# close the file
file.close()
