import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from util.data_loutr import NUMERICAL_VARIABLES, load_data

OPNR_CD_DF = load_data()

corr_df = OPNR_CD_DF[NUMERICAL_VARIABLES].dropna().corr()
fig, ax = plt.subplots(1, 1, figsize=(12,12))
img = ax.imshow(corr_df)
ax.set_xticks(np.arange(len(NUMERICAL_VARIABLES)))
ax.set_yticks(np.arange(len(NUMERICAL_VARIABLES)))
ax.set_xticklabels(NUMERICAL_VARIABLES)
ax.set_yticklabels(NUMERICAL_VARIABLES)


# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(NUMERICAL_VARIABLES)):
    for j in range(len(NUMERICAL_VARIABLES)):
        text = ax.text(j, i, f'{corr_df.loc[NUMERICAL_VARIABLES[i]][NUMERICAL_VARIABLES[j]]:.1%}',
                       ha="center", va="center", color="w")

fig.colorbar(img)
plt.tight_layout()
plt.show()

pca = PCA(n_components=6)
pca.fit(corr_df)
pca.explained_variance_ratio_.sum()
print(pca.singular_values_)
pca.components_.T * np.sqrt(pca.explained_variance_)

pd.DataFrame(pca.components_, columns=NUMERICAL_VARIABLES)
