import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


team_by_zone = pd.read_csv("Team_Shots_by_Zone.csv")

variables = [c for c in team_by_zone.columns if '_PERC_TOT' in c]
X = team_by_zone[variables].copy()

pca = PCA(n_components = len(variables))
pca.fit(X)

plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()

components = pd.DataFrame({'feature': variables})

for i in range(len(variables)):
    components['component_' + str(i+1)] = pca.components_[i,:]

components.to_csv("team_pca_components.csv", index = False)


fit = pca.transform(X)


team_by_zone['pca_1'] = fit[:,0]
team_by_zone['pca_2'] = fit[:,1]

team_by_zone.to_csv("Team_Shots_by_Zone.csv", index = False)
