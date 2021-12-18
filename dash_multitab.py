import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from util.data_loutr import NUMERICAL_VARIABLES, get_years, load_data, get_normalized_time_series
from util.filter import Filter
from views.view import View

opnrcd_df = load_data()
normalized_time_series = get_normalized_time_series()

all_years = get_years(opnrcd_df)

# Define all tabs
view_labels = ['Scatter', 'Heatmap', 'Correlation', 'Time Series', 'Treemap']
views = {f'tab-{i+1}-graph': View(label, f'tab-{i+1}-graph') for i, label in enumerate(view_labels)}

# Define all filters
filters = [
    Filter('x-axis', NUMERICAL_VARIABLES, default_selection=0),
    Filter('y-axis', NUMERICAL_VARIABLES, default_selection=1),
    Filter('Jahre', all_years, multi=True)
]
filter_inputs = [f.get_input() for f in filters]
filter_divs = [item for sublist in [f.get_label_dropdown() for f in filters] for item in sublist]


# TODO find a cool stylesheet
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)  # , external_stylesheets=external_stylesheets

app.layout = html.Div([
    dcc.Tabs(id="tabs-graph", value='tab-1-graph', children=[view.get_tab() for label, view in views.items()]),
    html.Div(filter_divs),
    html.Div(id='tabs-content-graph')
])

@app.callback(
    Output('tabs-content-graph', 'children'),
    Output('x-axis-select', 'style'),
    Output('x-axis-select-label', 'style'),
    Output('y-axis-select', 'style'),
    Output('y-axis-select-label', 'style'),
    Input('tabs-graph', 'value'),
    *filter_inputs
)
def render_content(tab, x_axis_name, y_axis_name, years):
    # select view based on tab selection
    view = views[tab]
    # generate figure
    view.generate_fig(opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years)
    return view.get_div()


if __name__ == '__main__':
    app.run_server(debug=True)
