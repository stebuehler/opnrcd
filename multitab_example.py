import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

from util.data_loutr import NUMERICAL_VARIABLES, load_data

OPNR_CD_DF = load_data()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # html.H1('Dash Tabs component demo'),
    html.Div([
        html.Label(['x-axis:'], style={'font-weight': 'bold', "text-align": "left"}),
        dcc.Dropdown(
            id='x-axis-select', options=[{'label': i, 'value': i} for i in NUMERICAL_VARIABLES],
            value=NUMERICAL_VARIABLES[0], style={'width': '50%'}
        ),
        html.Label(['y-axis:'], style={'font-weight': 'bold', "text-align": "left"}),
        dcc.Dropdown(
            id='y-axis-select', options=[{'label': i, 'value': i} for i in NUMERICAL_VARIABLES],
            value=NUMERICAL_VARIABLES[1], style={'width': '50%'})
    ]),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Scatter', value='tab-1-example-graph'),
        dcc.Tab(label='Heatmap', value='tab-2-example-graph'),
        dcc.Tab(label='Correlation', value='tab-3-example-graph')
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app.callback(
    Output('tabs-content-example-graph', 'children'),
    Input('tabs-example-graph', 'value'),
    Input('x-axis-select', 'value'),
    Input('y-axis-select', 'value')
)
def render_content(tab, x_axis_name, y_axis_name):
    if tab == 'tab-1-example-graph':
        fig = px.scatter(OPNR_CD_DF, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr')
        fig.update_layout(transition_duration=200)
        return html.Div([
            dcc.Graph(
                id='graph-1-tabs',
                figure=fig
            )])
    elif tab == 'tab-2-example-graph':
        heatmap_df = OPNR_CD_DF.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)
        fig = px.imshow(heatmap_df)
        fig.update_layout(transition_duration=200)
        return html.Div([
            dcc.Graph(
                id='graph-2-tabs',
                figure=fig
            )])
    elif tab == 'tab-3-example-graph':
        corr_df = OPNR_CD_DF[NUMERICAL_VARIABLES].dropna().corr()
        fig = px.imshow(corr_df)
        # fig.update_traces(textposition='inside')
        fig.update_layout(transition_duration=200)
        return html.Div([
            dcc.Graph(
                id='graph-3-tabs',
                figure=fig
            )])

if __name__ == '__main__':
    app.run_server(debug=True)