# import packages
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import Path

# Get path
path = Path.get_path()

# Write the name of the player file you'd like to perform
# PCA on here
file = "player_shots_by_zone_2018-19.csv"

# Read in the aggregated shot data
player_by_zone = pd.read_csv(path + file)

# Only grab the perc of total data
variables = [c for c in player_by_zone.columns if '_PERC_TOT' in c]
X = player_by_zone[variables].copy()

# Run pca and fit it
pca = PCA(n_components = len(variables))
pca.fit(X)

# Uncomment this to see the explained_variance_ratio_
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()

# Make a dataframe for the components.
components = pd.DataFrame({'feature': variables})


for i in range(len(variables)):
    components['component_' + str(i+1)] = pca.components_[i,:]

# Save components data fram to csv
components.to_csv(path + file[:-4] + "_comps.csv", index = False)

# Project the points to the hyperplane
fit = pca.transform(X)

# Record the first two coordinates for plotting
player_by_zone['pca_1'] = fit[:,0]
player_by_zone['pca_2'] = fit[:,1]
player_by_zone['pca_3'] = fit[:,2]

# Update Team_Shots_by_Zone.csv to include pca components
player_by_zone.to_csv(path + file, index = False)
