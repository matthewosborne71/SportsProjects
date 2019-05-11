import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


team_by_zone = pd.read_cs("Team_Shots_by_Zone.csv")
variables = team_by_zone.loc[0:len(team_by_zone),team_by_zone[team_by_zone.columns[2:]]]

pca = PCA(n_components = len(variables.columns))
pca.fit(team_by_zone)
