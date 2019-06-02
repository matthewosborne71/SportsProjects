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
 <li>ZONE_PERC_TOT - The percentage of the team's total shots that occurred in ZONE,</li>
 <li>ZONE_PERC_MADE - Of the shots that occurred in ZONE_i, the percentage that the team made.</li>
 <li>3_PERC_OF_TOT - What percent of the team's total shots were from 3,</li>
 <li>MID_PERC_OF_TOT - What percent of the team's total shots were from the mid range,</li>
 <li>CLOSE_PERC_OF_TOT - What percent of the team's total shots were from the paint.</li>
 </ul>
 
 #### PCA.py
 This code takes in the csv Team_Shots_by_Zone.csv that is output by OrganizeTeamData.py. It then takes only the PERC_TOT columns and runs that through a PCA. It will output a new csv file that records the component vectors from the pca, and alter Team_Shots_by_Zone.csv to include the first and second coordinates from the PCA projection. These are labeled pca_1 and pca_2. These are added for plotting purposes.
