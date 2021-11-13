import pandas as pd

NUMERICAL_VARIABLES = [
    'Künstlerische Relevanz (1-10)',
    'Musikalische Härte (1-10)',
    'Tanzbarkeit (1-10)',
    'Verblödungsfaktor (1-10)',
    'Nervofantigkeit (1-10)',
     'Weirdness (1-8)'
]


def load_data(strophen_only: bool=True):
    opnrcd_full_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
    if strophen_only:
        opnrcd_df = opnrcd_full_df[opnrcd_full_df["Strophe?"]]
    opnrcd_df = opnrcd_df.astype({"Jahr": str})
    return opnrcd_df