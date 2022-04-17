from abc import ABC
from dash import html, dcc
import dash_bootstrap_components as dbc
from util.filter import Filter

class AbstractView(ABC):
    def __init__(self):
        self.label = None
        self.display_options = dict()
        self.pre_display_options = dict()
        self.pre_display_option_target_outputs = []
        self.hide_filters_other_than_year = False
        self.starting_page = False

    def get_div(self, filters, display_options):
        active_filters = [f.name for f in filters] if not self.hide_filters_other_than_year else ['Jahr']
        active_display_options = [self.get_pre_display_option_id(label) for label in self.pre_display_options] + [self.get_display_option_id(label) for label in self.display_options]       
        active_filters_and_display_options = active_filters + active_display_options
        filter_style_list = [(('' if f.name in active_filters_and_display_options else 'None'), f.color) for f in (filters + display_options)]
        filter_display_style = [item for sublist in [[{'display': style, 'color': color}] + [{'display': style, 'color': color, 'font-weight': 'bold', 'text-align': 'left'}] for (style, color) in filter_style_list] for item in sublist]
        return filter_display_style

    def get_fig(self):
        if self.starting_page:
            return dbc.Col([
                html.Div([self.card])
                ]
            , width=6, xs=12, sm=10, md=6, lg=6, xl=4)
        else:    
            return dbc.Col([
                html.Div([dcc.Graph(id=self.label, figure=self.fig)])
                ]
                , width=12, xs=12, sm=12, md=12, lg=12, xl=12)

    def get_tab(self):
        return dbc.Tab(tab_id=self.value, label=self.label)

    def add_display_option(self, label, options, default_selection: int=0, multi: bool=False, clearable: bool=False, color=None, toggle: bool=False):
        self.display_options[label] = Filter(label, options, tab_name=self.label, default_selection=default_selection, multi=multi, clearable=clearable, color=color, toggle=toggle)

    def add_pre_display_option(self, label, options=None, default_selection: int=0, multi: bool=False, clearable: bool=False, button: bool=False, button_text=None):
        self.pre_display_options[label] = Filter(label, options, tab_name=self.label, default_selection=default_selection, multi=multi, clearable=clearable, button=button, button_text=button_text)

    def get_display_option_id(self, label):
        filter = self.display_options[label]
        return filter.name

    def get_pre_display_option_id(self, label):
        filter = self.pre_display_options[label]
        return filter.name

    def display_options_list(self):
        return list(self.display_options.values())

    def pre_display_options_list(self):
        return list(self.pre_display_options.values())

    def apply_pre_display_options(self, df, **kwargs):
        return None

    def pre_display_option_target_output_list(self):
        return self.pre_display_option_target_outputs
