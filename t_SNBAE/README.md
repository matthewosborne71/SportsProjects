# t_SNBAE
#### Matthew Osborne, joint with Kevin Nowland

The goal of this project is to implement some dimensionality reduction techniques on team shot selection data to see if we can identify different offensive play styles.

### Code Descriptions

#### Data Collection &amp; Data Organization Code
##### GrabTeamData.py
This code uses `nba_api` to grab every shot taken by every team over the past five seasons.

##### OrganizeTeamData.py
This code will take the csv file that results from GrabTeamData.py and classifies every shot into one of 15 zones on the court. It will produce a csv file with the following columns:
 <ul>
 <li>TEAM_NAME - The team's name,</li>
 <li>Season - The season,</li>
 <li>ZONE_i_PERC_OF_TOTAL_SHOTS - The percentage of the team's total shots that occurred in ZONE_i,</li>
 <li>ZONE_i_PERC_MADE - Of the shots that occurred in ZONE_i, the percentage that the team made.</li>
 </ul>
