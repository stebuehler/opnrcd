import pandas as pd

NUMERICAL_VARIABLES = [
    'Künstlerische Relevanz (1-10)',
    'Musikalische Härte (1-10)',
    'Tanzbarkeit (1-10)',
    'Verblödungsfaktor (1-10)',
    'Nervofantigkeit (1-10)',
    'Weirdness (1-8)'
]

def load_data(strophen_only: bool=True) -> pd.DataFrame:
    opnrcd_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
    if strophen_only:
        opnrcd_df = opnrcd_df[opnrcd_df["Strophe?"]]
    opnrcd_df = opnrcd_df.astype({"Jahr": str})
    return opnrcd_df


def get_normalized_time_series(df) -> pd.DataFrame:
    df['Timestamp normalized'] = df['Timestamp sekunden'] / df.groupby('Jahr')['Dauer (s)'].transform('sum')
    df_ts = df[df['Strophe?']].set_index(['Timestamp normalized', 'Jahr'])[NUMERICAL_VARIABLES].unstack('Jahr').ffill()
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

# this is how I think it should look but it alters the timeseries data
def filter_df_with_filters_target(**kwargs):
    df = load_data(strophen_only=False)
    for column in kwargs:
        values = kwargs[column]
        df = df[df[column].isin(values)]
    mean_std_time_series = mean_hi_lo_over_years(get_normalized_time_series(df))
    # filter for strophen only
    df = df[df["Strophe?"]]
    return df, mean_std_time_series

# This is the version that works without altering the timeseries data when filtering
def filter_df_with_filters(**kwargs):
    df = load_data(strophen_only=False)
    time_series = get_normalized_time_series(df)
    # filter the nasty time series - currently only for years
    years = kwargs['Jahr']
    mean_std_time_series = mean_hi_lo_over_years(
            time_series.iloc[:, time_series.columns.get_level_values(level='Jahr').isin(years)]
            )
    # filtering of the std df is more straightforward
    df = df[df["Strophe?"]]
    for column in kwargs:
        values = kwargs[column]
        df = df[df[column].isin(values)]
    return df, mean_std_time_series