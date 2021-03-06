import pandas as pd

NUMERICAL_VARIABLES = [
    'Künstlerische Relevanz',
    'Musikalische Härte',
    'Tanzbarkeit',
    'Verblödungsfaktor',
    'Nervofantigkeit',
    'Weirdness'
]

def load_data(strophen_only: bool=True) -> pd.DataFrame:
    opnrcd_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
    opnrcd_df = map_baujahr(opnrcd_df)
    if strophen_only:
        opnrcd_df = opnrcd_df[opnrcd_df["Strophe?"]]
    opnrcd_df = opnrcd_df.astype({"Jahr": str})
    return opnrcd_df


def get_normalized_time_series(df) -> pd.DataFrame:
    df['Startzeit normalisiert'] = df['Startzeit (s)'] / df.groupby('Jahr')['Dauer (s)'].transform('sum')
    df_ts = df[df['Strophe?']].set_index(['Startzeit normalisiert', 'Jahr'])[NUMERICAL_VARIABLES].unstack('Jahr').ffill()
    # Add 1.0 as last time index
    series = df_ts.iloc[-1]
    series.name = 1.0
    return df_ts.append(series)


# This is a bit ugly... TODO check and refactor
def mean_hi_lo_over_years(normalized_time_series: pd.DataFrame) -> pd.DataFrame:
    mean_std_time_series = normalized_time_series.T.groupby(level=0).agg(['mean', 'std']).stack(level=0)
    mean_std_time_series['low'] = mean_std_time_series['mean'] - mean_std_time_series['std']
    mean_std_time_series['high'] = mean_std_time_series['mean'] + mean_std_time_series['std']
    mean_std_time_series = mean_std_time_series.drop(columns=['std']).unstack(level=0)
    mean_std_time_series.columns = mean_std_time_series.columns.reorder_levels(order=[1, 0])
    return mean_std_time_series[mean_std_time_series.columns.sort_values()]
    

def get_all_entries_for_column(column, df=None, strophen_only=True):
    df = load_data(strophen_only=strophen_only) if df is None else df
    entries = df[column].unique()
    entries.sort()
    return entries


def get_max_entry_for_column(column, df=None, strophen_only=True):
    df = load_data(strophen_only=strophen_only) if df is None else df
    return df[column].max()


def get_min_entry_for_column(column, df=None, strophen_only=True):
    df = load_data(strophen_only=strophen_only) if df is None else df
    return df[column].min()
    

def filter_df_with_filters(list_of_range_slider_columns, **kwargs):
    df = load_data(strophen_only=False)
    time_series = get_normalized_time_series(df)
    # filter the nasty time series - only for years
    years = kwargs['Jahr']
    mean_std_time_series = mean_hi_lo_over_years(
            time_series.iloc[:, time_series.columns.get_level_values(level='Jahr').isin(years)]
            )
    # filtering of the std df is more straightforward
    df = df[df["Strophe?"]]
    for column in kwargs:
        if column in list_of_range_slider_columns:
            df = df[df[column].between(kwargs[column][0], kwargs[column][1])]
        else:
            values = kwargs[column] 
            df = df[df[column].isin(values)]
    return df, mean_std_time_series, time_series

def map_baujahr(df):
    df['Baujahr mapped'] = df['Baujahr'].apply(lambda x: x if x > 1950 else 1950)
    return df