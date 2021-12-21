from abc import ABC, abstractmethod
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# For now the active filters are defined staticly
active_filter_dict = {
    'Scatter':  ['Block', 'Block', 'Block', 'None'], 
    'Heatmap': ['Block', 'Block', 'Block', 'Block'], 
    'Correlation': ['None', 'None', 'Block', 'None'], 
    'Time Series': ['Block', 'Block', 'Block', 'None'],
    'Treemap': ['Block', 'Block', 'None', 'Block']
}

class AstractView(ABC):
    def __init__(self, label, value):
        self.label = label
        self.value = value
        # Note that for each filter we need the same display-style dictionary twice, once for the label and once for the filter
        self.active_filters = [item for sublist in [[{'display': style}]*2 for style in active_filter_dict[self.label]] for item in sublist]

    @abstractmethod
    def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
        pass

    def get_div(self):
        return html.Div([dcc.Graph(id=self.label, figure=self.fig)]), *self.active_filters

    def get_tab(self):
        return dcc.Tab(label=self.label, value=self.value)
