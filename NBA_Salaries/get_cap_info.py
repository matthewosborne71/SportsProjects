## get_cap_info.py
## Written by: Matthew Osborne
## Date 12-20-20
#################
## This script will give you the NBA salary cap from 1985-2021
## by scraping basketball-reference using BeautifulSoup
##################

# import necessary packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import Comment

# Make the soup
url = "https://www.basketball-reference.com/contracts/salary-cap-history.html"
html = urlopen(url)
soup = BeautifulSoup(html,"html.parser")

# Find the salary cap history table
for c in soup.find_all(string=lambda text: isinstance(text, Comment)):
    if ("table" in c) and ("salary_cap_history" in c):
        table = BeautifulSoup(c,"html.parser").table

# Get the seasons and caps
years = table.find_all("th",{'data-stat':"year_id"})
caps = table.find_all("td",{'data-stat':"cap"})
table_data = zip(years[1:],caps)

# Write the data to file
file = open("Data/salary_caps.csv","w+")
file.write("year,cap\n")

for year,cap in table_data:
     file.write(year.text + "," + cap.text.replace(",","").replace("$","") + "\n")

# close the file
file.close()
