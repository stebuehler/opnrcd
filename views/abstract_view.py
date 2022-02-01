from abc import ABC
from dash import html, dcc
import dash_bootstrap_components as dbc
from util.filter import Filter

class AbstractView(ABC):
    def __init__(self):
        self.label = None
        self.display_options = dict()
        self.active_display_options = []
        pass

    # TODO uncomment this to apply the years filter first
    # @abstractmethod
    # def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
    #     self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]

    def get_div(self, filters):
        self.active_display_options = [self.get_display_option_id(label) for label in self.display_options]
        filter_style_list = [('Block' if f.name in self.active_display_options else 'None') for f in filters]
        filter_display_style = [item for sublist in [[{'display': style}]*2 for style in filter_style_list] for item in sublist]
        return html.Div([dcc.Graph(id=self.label, figure=self.fig)]), *filter_display_style

    def get_tab(self):
        return dbc.Tab(tab_id=self.value, label=self.label)

    def add_display_option(self, label, options, default_selection: int=0, multi: bool=False, clearable: bool=False):
        self.display_options[label] = Filter(label, options, tab_name=self.label, default_selection=default_selection, multi=multi, clearable=clearable)

    def get_display_option_id(self, display_option_label):
        filter = self.display_options[display_option_label]
        return filter.name

    def display_options_list(self):
        return list(self.display_options.values())