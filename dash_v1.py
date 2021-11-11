import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

opnrcd_full_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
opnrcd_df = opnrcd_full_df[opnrcd_full_df["Strophe?"]]  # Strophen only

app = dash.Dash(__name__)
server = app.server


def extract_years(df):
    years = df['Jahr'].unique()
    years.sort()
    years = np.append(years, np.array(['All']))
    years = years[::-1]
    return years

years = extract_years(opnrcd_df)
# numerical_variables = ['Künstlerische Relevanz (1-10)',
#                        'Musikalische Härte (1-10)',
#                        'Tanzbarkeit (1-10)',
#                        'Verblödungsfaktor (1-10)',
#                        'Nervofantigkeit (1-10)',
#                        'Weirdness (1-8)']

app.layout = html.Div([
    html.Div([dcc.Dropdown(id='year-select', options=[{'label': i, 'value': i} for i in years],
                           value='All', style={'width': '140px'})]),
    # html.Div([dcc.Dropdown(id='x-axis-select', options=[{'label': i, 'value': i} for i in numerical_variables],
    #                            value='Künstlerische Relevanz (1-10)', style={'width': '180px'})]),
    # html.Div([dcc.Dropdown(id='y-axis-select', options=[{'label': i, 'value': i} for i in numerical_variables],
    #                                value='Musikalische Härte (1-10)', style={'width': '180px'})]),
    dcc.Graph('scatterplot', config={'displayModeBar': False})])


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('year-select', 'value')]
     # Input('x-axis-select', 'value'),
     # Input('y-axis-select', 'value')]
)
def update_graph(year):
    import plotly.express as px
    df_for_plot = opnrcd_df[opnrcd_df['Jahr'] == int(year)] if year != 'All' else opnrcd_df
    return px.scatter(df_for_plot, x='Künstlerische Relevanz (1-10)', y='Musikalische Härte (1-10)',
                      size='Dauer (s)', color='Jahr')


if __name__ == '__main__':
    app.run_server(debug=False)
