import pandas as pd
import plotly.express as px

source_filename = 'source_data/OPNRCD_alltime_stats.csv'
opnrcd_full_df = pd.read_csv(source_filename)
nur_strophen_df = opnrcd_full_df[opnrcd_full_df["Strophe?"] == True]
jahres_totale_df = nur_strophen_df.groupby("Jahr", as_index = False).agg({"Dauer (s)": "sum", "Relevanz x Dauer": "sum", "Härte x Dauer": "sum"})
jahres_totale_df["Avg Relevanz"] = jahres_totale_df["Relevanz x Dauer"] / jahres_totale_df["Dauer (s)"]
jahres_totale_df["Avg Härte"] = jahres_totale_df["Härte x Dauer"] / jahres_totale_df["Dauer (s)"]
#fig = px.scatter(nur_strophen_df, x='Relevanz x Dauer', y='Härte x Dauer', color='Jahr')
fig = px.scatter(jahres_totale_df, x='Avg Relevanz', y='Avg Härte', color='Jahr')
fig.show()
x = 5
