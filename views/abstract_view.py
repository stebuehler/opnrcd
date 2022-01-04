from abc import ABC
import dash_core_components as dcc
import dash_html_components as html

class AbstractView(ABC):
    def __init__(self):
        pass

    # TODO uncomment this to apply the years filter first
    # @abstractmethod
    # def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
    #     self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]

    def get_div(self, filters):
        filter_style_list = [('Block' if f.name in self.active_filters else 'None') for f in filters]
        filter_display_style = [item for sublist in [[{'display': style}]*2 for style in filter_style_list] for item in sublist]
        return html.Div([dcc.Graph(id=self.label, figure=self.fig)]), *filter_display_style

    def get_tab(self):
        return dcc.Tab(label=self.label, value=self.value)
