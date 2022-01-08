import dash
from dash import Input, Output, dcc, html

from util.data_loutr import NUMERICAL_VARIABLES, get_years, load_data, get_normalized_time_series
from util.filter import Filter
from views.view_correlation import ViewCorrelation
from views.view_heatmap import ViewHeatmap
from views.view_scatter import ViewScatter
from views.view_time_series import ViewTimeSeries
from views.view_treemap import ViewTreemap

opnrcd_df = load_data()
normalized_time_series = get_normalized_time_series()

all_years = get_years(opnrcd_df)

# Define all tabs
views = [ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries(), ViewTreemap()]

# Define all filters
filters = [
    Filter('x-axis', NUMERICAL_VARIABLES),
    Filter('y-axis', NUMERICAL_VARIABLES, default_selection=1),
    Filter('Jahre', all_years, multi=True),
    Filter('Measure', ['Dauer (min)', 'Count']),
    Filter('Group by', ['Nationalität', 'Sprache', 'Baujahr']),
    Filter('Color', NUMERICAL_VARIABLES + ['Jahr', 'Baujahr'])
]
filter_inputs = [f.get_input() for f in filters]
filter_outputs = [item for sublist in [f.get_output() for f in filters] for item in sublist]
filter_divs = [item for sublist in [f.get_label_dropdown() for f in filters] for item in sublist]


# TODO find a cool stylesheet
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)  # , external_stylesheets=external_stylesheets
server = app.server
app.title = "OPNRCD-ANLTCS"

app.layout = html.Div([
    dcc.Tabs(id="tabs-graph", value='Scatter-graph', children=[view.get_tab() for view in views]),
    html.Div(filter_divs),
    html.Div(id='tabs-content-graph')
])

@app.callback(
    Output('tabs-content-graph', 'children'),
    *filter_outputs,
    Input('tabs-graph', 'value'),
    filter_inputs
)
def render_content(tab, *args):
    # create the function arguments dynamically from the filters, see https://community.plotly.com/t/how-to-elegantly-handle-a-very-large-number-of-input-state-in-callbacks/19228
    kwargs = dict(zip([f.name for f in filters], args))
    # select view based on tab selection
    view = [v for v in views if v.value == tab][0]
    # generate figure
    view.generate_fig(opnrcd_df, normalized_time_series, **kwargs)
    return view.get_div(filters)


if __name__ == '__main__':
    app.run_server(debug=True)
