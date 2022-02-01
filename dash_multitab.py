import dash
from dash import Input, Output, html, State
import dash_bootstrap_components as dbc

from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column, load_data, get_normalized_time_series
from util.filter import Filter
from util.content import offcanvas_content
from views.view_correlation import ViewCorrelation
from views.view_heatmap import ViewHeatmap
from views.view_radar import ViewRadar
from views.view_scatter import ViewScatter
from views.view_time_series import ViewTimeSeries
from views.view_treemap import ViewTreemap

opnrcd_df = load_data()
normalized_time_series = get_normalized_time_series()

all_years = get_all_entries_for_column('Jahr', df=opnrcd_df, strophen_only=True)
alle_sprachen = get_all_entries_for_column('Sprache', df=opnrcd_df, strophen_only=True)

# Define all tabs
# views = [ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries(), ViewTreemap(), ViewRadar()]
views = [ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries()]

# Filters - these go across tabs
filters = [
    Filter('Jahre', all_years, multi=True),
    Filter('Sprachen', alle_sprachen, multi=True),
]
filter_inputs = [f.get_input() for f in filters]
filter_divs = [f.get_label_dropdown() for f in filters]

# display options depend on tab - achieved by nested list in "display_option_div"
display_options = [f for v in views for f in v.display_options_list()]
display_option_inputs = [f.get_input() for v in views for f in v.display_options_list()]
display_option_outputs = [item for sublist in [f.get_output() for v in views for f in v.display_options_list()] for item in sublist]
display_option_divs = [[f.get_label_dropdown() for f in v.display_options_list()] for v in views]

# the actual app starts here
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.PULSE],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
    )
server = app.server
app.title = "OPNRCD-ANLTCS"

# and here comes the layout...
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("opnrcd.ch", href="https://www.opnrcd.ch/", target="_blank")),
            dbc.NavItem(dbc.NavLink("figg-di.ch", href="https://www.figg-di.ch/", target="_blank")),
            dbc.Button("hä?", id='button_open_offcanvas', color="primary", className="me-1"),
        ],
        brand="OPNRCD-ANLTCS",
        brand_href="#",
        color="primary",
        dark=True
    ),
    dbc.Offcanvas(
            offcanvas_content(),
            id="offcanvas",
            title="Was isch das für en Scheiss?",
            is_open=False,
            placement='start'
        ),
    dbc.Tabs([view.get_tab() for view in views], id='tabs', active_tab='Scatter-graph'),
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(filter_divs)
                ],
                title='Filters'
            ),
            dbc.AccordionItem(
                children = [dbc.Row(display_option_row) for display_option_row in display_option_divs],
                title='Display options'
            )
        ],
        start_collapsed=True,
        flush=True,
    ),
    dbc.Row(dbc.Col(html.Div(id='tabs-content-graph')))
])

@app.callback(
    Output('tabs-content-graph', 'children'),
    *display_option_outputs,
    Input('tabs', 'active_tab'),
    filter_inputs,
    display_option_inputs
)
def render_content(tab, *args):
    # create the function arguments dynamically from the filters, see https://community.plotly.com/t/how-to-elegantly-handle-a-very-large-number-of-input-state-in-callbacks/19228
    kwargs = dict(zip([f.name for f in filters] + [f.name for f in display_options], args))
    # select view based on tab selection
    view = [v for v in views if v.value == tab][0]
    # generate figure
    view.generate_fig(opnrcd_df, normalized_time_series, **kwargs)
    return view.get_div(display_options)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("button_open_offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
