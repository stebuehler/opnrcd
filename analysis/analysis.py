import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing

from util.data_loutr import NUMERICAL_VARIABLES, load_data, get_normalized_time_series, mean_hi_lo_over_years


# plot correlation heat map
def plot_correlation_heat_map(corr_df: pd.DataFrame) -> None:
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


normalized_time_series = get_normalized_time_series()

# plot time series for one category for each year -> messy!
selected_column = NUMERICAL_VARIABLES[0]
normalized_time_series[selected_column].plot(drawstyle='steps-pre')
plt.title(selected_column)
plt.show()

# plot mean band time series
mean_std_time_series = mean_hi_lo_over_years(normalized_time_series)
fig, ax = plt.subplots(len(NUMERICAL_VARIABLES), 1, figsize=(12,12))
for i in range(len(NUMERICAL_VARIABLES)):
    mean_std_time_series[NUMERICAL_VARIABLES[i]].plot(ax=ax[i], drawstyle='steps-pre')
    ax[i].set_ylabel(NUMERICAL_VARIABLES[i])
plt.show()

# Calculate & plot correlation
corr_df = load_data()[NUMERICAL_VARIABLES].dropna().corr()
plot_correlation_heat_map(corr_df)

# Preprocessing
full_df = load_data()
feature_df =full_df[NUMERICAL_VARIABLES].dropna()
scaler = preprocessing.StandardScaler().fit(feature_df)
# scaled feature space has zero mean and unit variance
features_scaled = scaler.transform(feature_df)

# PCA
for n_components in range(1, len(NUMERICAL_VARIABLES) + 1):
    pca = PCA(n_components=n_components)
    features_reduced = pca.fit_transform(features_scaled)
    features_predicted = pca.inverse_transform(features_reduced)
    feature_df_predicted = pd.DataFrame(features_predicted, columns=NUMERICAL_VARIABLES)

    distance_df = pd.DataFrame(features_scaled, columns=NUMERICAL_VARIABLES) - feature_df_predicted
    feature_df['distance'] = np.array(np.sqrt((distance_df**2).sum(axis=1)))
    mean_distance = np.sqrt((distance_df**2).sum(axis=1)).mean()
    explained_variance = pca.explained_variance_ratio_.sum()
    print(f'PCA with {n_components} components has avg(distance) = {mean_distance:.2f} and explained variance is {explained_variance:.1%}')
    full_df[f'distance_{n_components}'] = feature_df['distance']

assert full_df[f'distance_{len(NUMERICAL_VARIABLES)}'].max() < 1.e-10



sort_by_n_components = 5
# Top & bottom five Strophen by distance to prediction
full_df[full_df['Jahr'] != '2021'].sort_values(f'distance_{sort_by_n_components}')[['Jahr', 'Künstler', 'Titel'] + [f'distance_{n_components}' for n_components in range(1, len(NUMERICAL_VARIABLES))]]

# average distance per year
full_df[full_df['Jahr'] != '2021'].groupby('Jahr').mean()[[f'distance_{n_components}' for n_components in range(1, len(NUMERICAL_VARIABLES))]].sort_values(f'distance_{sort_by_n_components}')


