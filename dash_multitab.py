import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries, load_data, get_normalized_time_series
from util.filter import Filter
from views.view_correlation import ViewCorrelation
from views.view_heatmap import ViewHeatmap
from views.view_parallel_category import ViewParallelCategory
from views.view_radar import ViewRadar
from views.view_scatter import ViewScatter
from views.view_time_series import ViewTimeSeries
from views.view_treemap import ViewTreemap

opnrcd_df = load_data()
normalized_time_series = get_normalized_time_series()

all_years = get_all_entries(opnrcd_df, 'Jahr')
alle_sprachen = get_all_entries(opnrcd_df, 'Sprache')

# Define all tabs
views = [ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries(), ViewTreemap(), ViewParallelCategory(), ViewRadar()]

# Define all filters
filters = [
    Filter('x-axis', NUMERICAL_VARIABLES + ['Timestamp sekunden']),
    Filter('y-axis', NUMERICAL_VARIABLES + ['Timestamp sekunden'], default_selection=1),
    Filter('Measure', ['Dauer (min)', 'Count']),
    Filter('Group by', ['Jahr', 'Nationalität', 'Sprache', 'Baujahr', 'Künstler', 'Titel']),
    Filter('Color', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Jahr', 'Baujahr'], default_selection=2),
    Filter('Level of detail', ['Full (1-10)', 'Reduced (Low-Mid-High)']),
    Filter('Jahre', all_years, multi=True),
    Filter('Sprachen', alle_sprachen, multi=True),
    Filter('Variables to show', NUMERICAL_VARIABLES, multi=True)
]
filter_inputs = [f.get_input() for f in filters]
filter_outputs = [item for sublist in [f.get_output() for f in filters] for item in sublist]
filter_divs = [f.get_label_dropdown() for f in filters]


# TODO find a cool stylesheet
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
    )
server = app.server
app.title = "OPNRCD-ANLTCS"

app.layout = dbc.Container([
    dbc.Tabs([view.get_tab() for view in views], id='tabs', active_tab='Scatter-graph'),
    dbc.Row(filter_divs),
    dbc.Row(dbc.Col(html.Div(id='tabs-content-graph')))
])

@app.callback(
    Output('tabs-content-graph', 'children'),
    *filter_outputs,
    Input('tabs', 'active_tab'),
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
