from abc import ABC
from dash import html, dcc
import dash_bootstrap_components as dbc
from util.filter import Filter

class AbstractView(ABC):
    def __init__(self):
        self.label = None
        self.display_options = dict()
        self.pre_display_options = dict()

    def get_div(self, filters):
        active_display_options = [self.get_pre_display_option_id(label) for label in self.pre_display_options] + [self.get_display_option_id(label) for label in self.display_options]
        filter_style_list = [('Block' if f.name in active_display_options else 'None') for f in filters]
        filter_display_style = [item for sublist in [[{'display': style}]*2 for style in filter_style_list] for item in sublist]
        return filter_display_style

    def get_fig(self):
        return html.Div([dcc.Graph(id=self.label, figure=self.fig)])

    def get_tab(self):
        return dbc.Tab(tab_id=self.value, label=self.label)

    def add_display_option(self, label, options, default_selection: int=0, multi: bool=False, clearable: bool=False):
        self.display_options[label] = Filter(label, options, tab_name=self.label, default_selection=default_selection, multi=multi, clearable=clearable)

    def add_pre_display_option(self, label, options, default_selection: int=0, multi: bool=False, clearable: bool=False):
        self.pre_display_options[label] = Filter(label, options, tab_name=self.label, default_selection=default_selection, multi=multi, clearable=clearable)

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