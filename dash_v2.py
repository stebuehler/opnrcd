import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

opnrcd_full_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
opnrcd_df = opnrcd_full_df[opnrcd_full_df["Strophe?"]]  # Strophen only
opnrcd_df = opnrcd_df.astype({"Jahr": str})

app = dash.Dash(__name__)
server = app.server

numerical_variables = ['Künstlerische Relevanz (1-10)',
                       'Musikalische Härte (1-10)',
                       'Tanzbarkeit (1-10)',
                       'Verblödungsfaktor (1-10)',
                       'Nervofantigkeit (1-10)',
                       'Weirdness (1-8)']

app.layout = html.Div([
    html.Div([
        html.Label(['x-axis:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='x-axis-select', options=[{'label': i, 'value': i} for i in numerical_variables],
                           value='Künstlerische Relevanz (1-10)', style={'width': '50%'}),
        html.Label(['y-axis:'], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='y-axis-select', options=[{'label': i, 'value': i} for i in numerical_variables],
                           value='Musikalische Härte (1-10)', style={'width': '50%'})
    ]),
    dcc.Graph('scatterplot', config={'displayModeBar': False})])


@app.callback(
    Output('scatterplot', 'figure'),
    Input('x-axis-select', 'value'),
    Input('y-axis-select', 'value'))
def update_graph(x_axis_name, y_axis_name):
    import plotly.express as px
    fig = px.scatter(opnrcd_df, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr')
    fig.update_layout(transition_duration=200)
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
