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
 <li>TEAM_ID - The team's id, this allows for tracking a team across name changes</li>
 <li>TEAM_NAME - The team's name,</li>
 <li>Season - The season,</li>
 <li>ZONE_PERC_TOT - The percentage of the team's total shots that occurred in ZONE,</li>
 <li>ZONE_PERC_MADE - Of the shots that occurred in ZONE, the percentage that the team made.</li>
 <li>3_PERC_OF_TOT - What percent of the team's total shots were from 3,</li>
 <li>MID_PERC_OF_TOT - What percent of the team's total shots were from the mid range,</li>
 <li>CLOSE_PERC_OF_TOT - What percent of the team's total shots were from the paint.</li>
 </ul>
 
##### OrganizePlayerData.py
This code will take the csv file that results from GrabTeamData.py and classifies every shot into one of 15 zones on the court. It will produce a csv file with the following columns:
 <ul>
 <li>PLAYER_NAME - The player's name,</li>
 <li>ZONE_PERC_TOT - The percentage of the player's total shots that occurred in ZONE,</li>
 <li>ZONE_PERC_MADE - Of the shots that occurred in ZONE, the percentage that the team made.</li>
 </ul>
 
#### *PCA.py
This code performs PCA on the ZONE_PERC_TOT columns from the Aggregated csvs produced by OrganizeTeamData.py and OrganizePlayerData.py.
