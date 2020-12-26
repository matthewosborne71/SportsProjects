## get_cap_info.py
## Written by: Matthew Osborne
## Date 12-20-20
#################
## This script will give you the team endpoints from the 1985-2021 NBA seasons
## by scraping basketball-reference using BeautifulSoup
##################

## import packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import Comment

# open the file that stores the data
file = open("Data/team_endpoints.csv","w+")

# write column headers
file.write("season,team,endpoint\n")

# These are the urls minus the year
url_start = "https://www.basketball-reference.com/leagues/NBA_"
url_end = "_standings.html"

# for each season 1985-2020
for season in [str(year) for year in range(1985,2021)]:
    print("getting team endpoints for " + season)
    # make soup
    url = url_start + season + url_end
    html = urlopen(url)
    soup = BeautifulSoup(html,"html.parser")

    # find the expanded_standings table
    for c in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if ("table" in c) and ("expanded_standings" in c):
            table = BeautifulSoup(c,"html.parser").table

    # record the data
    for td in table.tbody.find_all("td",{'data-stat':"team_name"}):
        file.write(season + "," + td.text + "," + td.a["href"] + "\n")

# 2021 had a different endpoint because the season hadn't started yet
print("getting team endpoints for 2021")
url = "https://www.basketball-reference.com/leagues/NBA_2021_standings.html"
html = urlopen(url)
soup = BeautifulSoup(html,"html.parser")

east_table = soup.find('table',{'id':"confs_standings_E"})
west_table = soup.find('table',{'id':"confs_standings_W"})

for th in east_table.find_all('th',{'data-stat':"team_name"})[1:]:
    file.write("2021," + th.text.split("(")[0].strip() + "," + th.a["href"] + "\n")

for th in west_table.find_all('th',{'data-stat':"team_name"})[1:]:
    file.write("2021," + th.text.split("(")[0].strip() + "," + th.a["href"] + "\n")

# close the file
file.close()
