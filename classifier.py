import pandas as pd
from sklearn.decomposition import PCA

from util.data_loutr import load_data, NUMERICAL_VARIABLES


def define_binning(df, num_vars, mode):
    assert mode in ['std', 'quantiles', 'fixed']
    for num_var in num_vars:
        labels = ['low', 'medium', 'high']
        if mode == 'std':
            stats = df[num_var].agg(['mean', 'std'])
            df[num_var + '_binned'] = pd.cut(df[num_var], [df[num_var].min(), stats['mean'] - stats['std'], stats['mean'] + stats['std'], df[num_var].max()], labels=labels)
        if mode == 'quantiles':
            df[num_var + '_binned'] = pd.qcut(df[num_var], q=[0, 0.25, 0.75, 1.0], labels=labels)
        if mode == 'fixed':
            bins = [1, 3.5, 5.5, 8] if 'Weirdness' in num_var else [1, 4.5, 6.5, 10]
            df[num_var + '_binned'] = pd.cut(df[num_var], bins, labels=labels)


def get_feature_df(df, measure, num_vars, time_weighted: bool = False):
    assert measure in ['count', 'count_relativ', 'Dauer (s)', 'dauer_relativ']
    dfs = []
    if time_weighted:
        df[measure + '_time_weighted'] = df[measure] * df['time_weight']
        measure = measure + '_time_weighted'
    for num_var in num_vars:
        aux = df.groupby(['Jahr', num_var + '_binned']).sum()[measure].unstack(num_var + '_binned')[['low', 'high']]
        aux.columns = [num_var + '_low', num_var + '_high']
        dfs.append(aux)

    return pd.concat(dfs, axis=1)


def prepare_data(measure, mode, time_weighted):
    df = load_data()
    df = df.rename(columns={k: k.replace(' (1-10)', '').replace(' (1-8)', '') for k in NUMERICAL_VARIABLES})
    num_vars = [num_var.replace(' (1-10)', '').replace(' (1-8)', '') for num_var in NUMERICAL_VARIABLES]
    df['dauer_relativ'] = df[['Dauer (s)', 'Jahr']].groupby('Jahr').transform('sum')
    df['dauer_relativ'] = df['Dauer (s)'] / df['dauer_relativ']
    df['count'] = 1.0
    df['count_relativ'] = df[['count', 'Jahr']].groupby('Jahr').transform('sum')
    df['count_relativ'] = df['count'] / df['count_relativ']
    df['end_time'] = df['Startzeit (s)'] + df['Dauer (s)']
    df['time_weight'] = df[['Jahr', 'end_time']].groupby('Jahr').transform('max')
    df['time_weight'] = (df['Startzeit (s)'] + df['Dauer (s)'] / 2.0) / df['time_weight']
    df['time_weight'] = df['time_weight'].apply(lambda x: 1-x**2/2.0)
    define_binning(df, num_vars, mode)
    return get_feature_df(df, measure, num_vars, time_weighted)


# fix PCA to two components -> count_relativ and fixed binning maximizes explained variance
n_components = 2

for measure in ['count', 'count_relativ', 'Dauer (s)', 'dauer_relativ'][1:2]:
    for mode in ['std', 'quantiles', 'fixed'][-1:]:
        features = prepare_data(measure, mode, True)
        pca = PCA(n_components=n_components)
        pca.fit(features)
        reduced_features = pd.DataFrame(pca.components_.T, index=features.columns)
        print(f'PCA with {n_components} components, {measure} and {mode} has Explained Variance Ratio: {pca.explained_variance_ratio_.sum():.1%}')

# The composition of the main components are easy to interpret as 'weirder & nerviger Blödsinn' & 'simple Party'
for pca_component in range(n_components):
    print(reduced_features[[pca_component]].assign(abs=abs(reduced_features[pca_component])).sort_values('abs', ascending=False)[pca_component].head(5))

# This is are the reduced features
features_reduced = pd.DataFrame(pca.fit_transform(features), index=features.index, columns=['weirder & nerviger Blödsinn', 'simple Party'])

# plotting
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
features_reduced.plot('weirder & nerviger Blödsinn', 'simple Party', kind='scatter', ax=ax)
for k, v in features_reduced.iterrows():
    ax.annotate(k, v)
fig.show()

# Interpretation
# - mir der Zeit wurde die OPNRCD immer mehr zu weirder & nerviger Blödsinn
# - 2009 war weder weirder & nerviger Blödsinn noch simple Party
# - 2010 & 2011 waren die simplen Partyjahre ohne weirden & nervigen Blödsinn
# - abgesehen von 2010 & 2011 war die Partytauglichkeit eher durchmischt, mal mehr mal weniger


# --------------------------------------
# cut classification -> decision trees:
# --------------------------------------
df = load_data()
df = df.rename(columns={k: k.replace(' (1-10)', '').replace(' (1-8)', '') for k in NUMERICAL_VARIABLES})
num_vars = [num_var.replace(' (1-10)', '').replace(' (1-8)', '') for num_var in NUMERICAL_VARIABLES]
df['dauer_relativ'] = df[['Dauer (s)', 'Jahr']].groupby('Jahr').transform('sum')
df['dauer_relativ'] = df['Dauer (s)'] / df['dauer_relativ']
df['count'] = 1.0
df['count_relativ'] = df[['count', 'Jahr']].groupby('Jahr').transform('sum')
df['count_relativ'] = df['count'] / df['count_relativ']
df['end_time'] = df['Startzeit (s)'] + df['Dauer (s)']
df['time_weight'] = df[['Jahr', 'end_time']].groupby('Jahr').transform('max')
df['time_weight'] = (df['Startzeit (s)'] + df['Dauer (s)'] / 2.0) / df['time_weight']
df['time_weight'] = df['time_weight'].apply(lambda x: 1-x/2.0)

df['dauer_relativ_time_weighted'] = df['dauer_relativ'] * df['time_weight']

NUMBER_OF_YEARS = len(df['Jahr'].unique())


def calculate_score(cut, cut_series, year):
    series1 = df[condition].groupby('Jahr').sum()[measure]
    series2 = df[~condition].groupby('Jahr').sum()[measure]
    tp = series1[series1.index == year].sum()
    tn = series2[series2.index != year].sum()/(NUMBER_OF_YEARS-1)  # division by NUMBER_OF_YEARS-1 should account for imbalance correction
    fp = series1[series1.index != year].sum()/(NUMBER_OF_YEARS-1)
    fn = series2[series2.index == year].sum()
    score = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0.0 else 0.0  # accuracy with imbalance correction
    # print(f'{year}: {score:.3f}')
    if score > max_dict[year][-1]:
        max_dict[year][-1] = score
        cut_series_dict[year] = cut_series
        cut_dict[year] = cut_dict_fix[year] + ", " + cut


cut_dict = {year: '' for year in df['Jahr'].unique()}
cut_series_dict = {year: df[num_vars[0]] > 0 for year in df['Jahr'].unique()}
max_dict = {year: [] for year in df['Jahr'].unique()}

measure = 'dauer_relativ_time_weighted'

check = True

while check:
    cut_dict_fix = cut_dict.copy()
    cut_series_dict_fix = cut_series_dict.copy()
    for year in df['Jahr'].unique():
        max_dict[year].append(-1.0)
    max_dict_fix = max_dict.copy()

    for num_var in num_vars:
        print(f'Split Nr. {len(list(max_dict.values())[0])} on {num_var}')
        for val in list(df[num_var].sort_values().unique()):
            cut = f'{num_var} > {val}'
            for year in df['Jahr'].unique():
                condition = cut_series_dict_fix[year] & (df[num_var] > val)
                calculate_score(cut, condition, year)

            cut = f'{num_var} < {val}'
            for year in df['Jahr'].unique():
                condition = cut_series_dict_fix[year] & (df[num_var] < val)
                calculate_score(cut, condition, year)

    check = False
    for year, scores in max_dict.items():
        if len(scores) < 2:
            check = True
        elif scores[-1] > max(scores[:-1]):
            print(f'{year}:  {max(scores[:-1]):.1%} -> {scores[-1]:.1%}')
            check = True

cut_df = pd.DataFrame.from_dict(cut_dict.items()).rename(columns={0: 'Jahr', 1: 'cut'}).sort_values('Jahr').set_index('Jahr')
score_df = pd.DataFrame.from_dict(max_dict.items()).rename(columns={0: 'Jahr', 1: 'score'}).sort_values('Jahr').set_index('Jahr')
cut_score_df = pd.merge(cut_df, score_df, left_index=True, right_index=True)

# --------------------------
# Forward looking cuts
# --------------------------
# cut_dict = {year: '' for year in df['Jahr'].unique()}
# max_dict = {year: -1.0 for year in df['Jahr'].unique()}

# for i, num_var in enumerate(num_vars):
#     for j, num_var2 in enumerate(num_vars):
#         if j >= i:
#             for val in list(df[num_var].sort_values().unique())[:-1]:
#                 for val2 in list(df[num_var].sort_values().unique())[:-1]:
#                     cut = f'{num_var} > {val} and {num_var2} > {val2}'
#                     series1 = df[(df[num_var] > val) & (df[num_var2] > val2)].groupby('Jahr').sum()[measure]
#                     series2 = df[(df[num_var] <= val) | (df[num_var2] <= val2)].groupby('Jahr').sum()[measure]
#                     calculate_score(series1, series2, cut)
#
#                     cut = f'{num_var} > {val} and {num_var2} < {val2}'
#                     series1 = df[(df[num_var] > val) & (df[num_var2] < val2)].groupby('Jahr').sum()[measure]
#                     series2 = df[(df[num_var] <= val) | (df[num_var2] >= val2)].groupby('Jahr').sum()[measure]
#                     calculate_score(series1, series2, cut)
#
#                     cut = f'{num_var} < {val} and {num_var2} > {val2}'
#                     series1 = df[(df[num_var] < val) & (df[num_var2] > val2)].groupby('Jahr').sum()[measure]
#                     series2 = df[(df[num_var] >= val) | (df[num_var2] <= val2)].groupby('Jahr').sum()[measure]
#                     calculate_score(series1, series2, cut)
#
#                     cut = f'{num_var} < {val} and {num_var2} < {val2}'
#                     series1 = df[(df[num_var] < val) & (df[num_var2] < val2)].groupby('Jahr').sum()[measure]
#                     series2 = df[(df[num_var] >= val) | (df[num_var2] >= val2)].groupby('Jahr').sum()[measure]
#                     calculate_score(series1, series2, cut)

features = prepare_data('dauer_relativ', 'quantiles', True)

features[features.columns[10:12]].plot()
plt.show()
