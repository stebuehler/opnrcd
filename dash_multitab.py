import dash
from dash import Input, Output, html, State
import dash_bootstrap_components as dbc

from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column, load_data, get_normalized_time_series, filter_df_with_filters
from util.filter import Filter
from util.content import offcanvas_content
from views.view_correlation import ViewCorrelation
from views.view_heatmap import ViewHeatmap
from views.view_radar import ViewRadar
from views.view_scatter import ViewScatter
from views.view_time_series import ViewTimeSeries
from views.view_treemap import ViewTreemap
from views.view_start_page import ViewStartPage

# Define all tabs
# views = [ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries(), ViewTreemap(), ViewRadar()]
views = [ViewStartPage(), ViewRadar(), ViewTreemap(), ViewScatter(), ViewHeatmap(), ViewCorrelation(), ViewTimeSeries()]

# Filters - these go across tabs
filters = [
    Filter('Jahre', get_all_entries_for_column('Jahr', strophen_only=True), column_name='Jahr', multi=True),
    Filter('Sprachen', get_all_entries_for_column('Sprache', strophen_only=True), column_name='Sprache', multi=True),
    Filter('Nationalitäten', get_all_entries_for_column('Nationalität', strophen_only=True), column_name='Nationalität', multi=True),
]
filter_inputs = [f.get_input() for f in filters]
filter_outputs = [item for sublist in [f.get_output() for f in filters] for item in sublist]
filter_divs = [f.get_label_dropdown() for f in filters]

# "pre" display options. When a first callback is needed to determine the content of the display options
pre_display_options = [f for v in views for f in v.pre_display_options_list()]
pre_display_option_inputs = [f.get_input() for v in views for f in v.pre_display_options_list()]
pre_display_option_display_outputs = [item for sublist in [f.get_output() for v in views for f in v.pre_display_options_list()] for item in sublist]
pre_display_option_target_outputs = [output for v in views for output in v.pre_display_option_target_output_list()]
pre_display_option_divs = [[f.get_label_dropdown() for f in v.pre_display_options_list()] for v in views]

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
app.title = "OPNRCD-ANLTK"

# and here comes the layout...
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("opnrcd.ch", href="https://www.opnrcd.ch/", target="_blank")),
            dbc.NavItem(dbc.NavLink("figg-di.ch", href="https://www.figg-di.ch/", target="_blank")),
            dbc.Button("hä?", id='button_open_offcanvas', color="primary", className="me-1"),
        ],
        brand="OPNRCD-ANLTK",
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
    dbc.Tabs([view.get_tab() for view in views], id='tabs', active_tab=views[0].value),
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(filter_divs)
                ],
                title='Filter'
            ),
            dbc.AccordionItem(
                children = [dbc.Row(pre_display_option_row) for pre_display_option_row in pre_display_option_divs]
                 + [dbc.Row(display_option_row) for display_option_row in display_option_divs],
                title='Anzeigeoptionen'
            )
        ],
        start_collapsed=True,
        flush=True,
    ),
    dbc.Row(dbc.Col(html.Div(id='tabs-content-graph')), justify="center")
])

# this callback sets the display styles of all display options (invisible except the ones for the current tab)
@app.callback(
    *filter_outputs,
    *pre_display_option_display_outputs,
    *display_option_outputs,
    Input('tabs', 'active_tab'),
)
def apply_tab_filters(tab):
    view = [v for v in views if v.value == tab][0]
    return view.get_div(filters, pre_display_options + display_options)

# this is the "pre" callback for the display options that need it.
@app.callback(
    *pre_display_option_target_outputs,
    filter_inputs,
    pre_display_option_inputs
)
def apply_pre_display_options(*args):
    kwargs_all = dict(zip([f.name for f in filters] + [f.name for f in pre_display_options], args))
    kwargs_for_df_filtering = {f.name: kwargs_all[f.name] for f in filters}
    kwargs_for_fig = {name: kwargs_all[name] for name in kwargs_all if name not in kwargs_for_df_filtering}
    df, time_series_data = filter_df_with_filters(**kwargs_for_df_filtering)
    return_list = None
    for view in views:
        output_this_view = view.apply_pre_display_options(df, **kwargs_for_fig)
        if output_this_view:
            if return_list:
                return_list = return_list + output_this_view
            else:
                return_list = output_this_view
    return return_list

# this is the main callback for the graph(s), depending on the tab
@app.callback(
    Output('tabs-content-graph', 'children'),
    Input('tabs', 'active_tab'),
    filter_inputs,
    pre_display_option_inputs,
    display_option_inputs
)
def render_content(tab, *args):
    # create the function arguments dynamically from the filters, see https://community.plotly.com/t/how-to-elegantly-handle-a-very-large-number-of-input-state-in-callbacks/19228
    kwargs_all = dict(zip([f.name for f in filters] + [f.name for f in pre_display_options] + [f.name for f in display_options], args))
    kwargs_for_df_filtering = {f.name: kwargs_all[f.name] for f in filters}
    kwargs_for_fig = {name: kwargs_all[name] for name in kwargs_all if name not in kwargs_for_df_filtering}
    # df filtering
    df, time_series_data = filter_df_with_filters(**kwargs_for_df_filtering)
    # select view based on tab selection
    view = [v for v in views if v.value == tab][0]
    # generate figure
    view.generate_fig(df, time_series_data, **kwargs_for_fig)
    return view.get_fig()

# aux callback for the offcanvas (help "hä" page)
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
