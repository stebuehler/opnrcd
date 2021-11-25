import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util.data_loutr import NUMERICAL_VARIABLES, load_data, get_normalized_time_series, mean_hi_lo_over_years

opnrcd_df = load_data()
normalized_time_series = get_normalized_time_series()
mean_std_time_series = mean_hi_lo_over_years(normalized_time_series)


# plot mean band time series
def get_time_series_fig(x_axis_name, y_axis_name):
    fig = make_subplots(rows=2, cols=1)

    x = list(mean_std_time_series.index)

    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[x_axis_name]['high']) + list(mean_std_time_series[x_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[y_axis_name]['high']) + list(mean_std_time_series[y_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name=y_axis_name,
        showlegend=False
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[x_axis_name]['mean'],
        line_color='rgb(0,100,80)',
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[y_axis_name]['mean'],
        line_color='rgb(0,176,246)',
        name=y_axis_name
    ), row=2, col=1)
    fig.update_traces(mode='lines')
    return fig


# TODO find a cool stylesheet
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)  # , external_stylesheets=external_stylesheets

app.layout = html.Div([
    dcc.Tabs(id="tabs-graph", value='tab-1-graph', children=[
        dcc.Tab(label='Scatter', value='tab-1-graph'),
        dcc.Tab(label='Heatmap', value='tab-2-graph'),
        dcc.Tab(label='Correlation', value='tab-3-graph'),
        dcc.Tab(label='Time Series', value='tab-4-graph'),
        dcc.Tab(label='Treemap', value='tab-5-graph')
    ]),
    # TODO these dropdowns should depend on tab
    html.Div([
        html.Label(['x-axis:'], style={'font-weight': 'bold', "text-align": "left"}),
        dcc.Dropdown(
            id='x-axis-select', options=[{'label': i, 'value': i} for i in NUMERICAL_VARIABLES],
            value=NUMERICAL_VARIABLES[0]
        ),
        html.Label(['y-axis:'], style={'font-weight': 'bold', "text-align": "left"}),
        dcc.Dropdown(
            id='y-axis-select', options=[{'label': i, 'value': i} for i in NUMERICAL_VARIABLES],
            value=NUMERICAL_VARIABLES[1]
        )
    ]),
    html.Div(id='tabs-content-graph')
])

@app.callback(
    Output('tabs-content-graph', 'children'),
    Input('tabs-graph', 'value'),
    Input('x-axis-select', 'value'),
    Input('y-axis-select', 'value')
)
def render_content(tab, x_axis_name, y_axis_name):
    if tab == 'tab-1-graph':
        fig = px.scatter(opnrcd_df, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr')
        fig.update_layout(transition_duration=200)
        return html.Div([dcc.Graph(id='graph-1-tabs', figure=fig)])
    elif tab == 'tab-2-graph':
        # TODO option to select value of heatmap: count / duration
        # heatmap_df = opnrcd_df.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)  # count
        heatmap_df = opnrcd_df.groupby([x_axis_name, y_axis_name]).sum()['Dauer (s)'].unstack(x_axis_name).fillna(0.0)  # duration
        fig = px.imshow(heatmap_df)
        fig.update_layout(transition_duration=200)
        return html.Div([dcc.Graph(id='graph-2-tabs', figure=fig)])
    elif tab == 'tab-3-graph':
        corr_df = opnrcd_df[NUMERICAL_VARIABLES].dropna().corr()
        fig = px.imshow(corr_df)
        # TODO find a way to show correlation numbers in heat map
        # fig.update_traces(textposition='inside')
        fig.update_layout(transition_duration=200)
        return html.Div([dcc.Graph(id='graph-3-tabs',figure=fig)])
    elif tab == 'tab-4-graph':
        fig = get_time_series_fig(x_axis_name, y_axis_name)
        return html.Div([dcc.Graph(id='graph-4-tabs',figure=fig)])
    elif tab == 'tab-5-graph':
        # TODO Let user chose if grouping by Country or different attribute (Baujahr etc.)
        # TODO Different levels of how deep to go into hierarchy (e.g. stop at country but can also go until Künstler)
        # TODO Choice of which OPNRCDs to include.
        # TODO choice whether to include skits or not.
        fig = px.treemap(opnrcd_df, path=['Kontinent', 'Nationalität'], values='Dauer (s)')
        fig.data[0].hovertemplate = '%{label}<br>%{value}'
        return html.Div([dcc.Graph(id='graph-5-tabs', figure=fig)])


if __name__ == '__main__':
    app.run_server(debug=True)
