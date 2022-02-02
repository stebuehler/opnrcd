from views.abstract_view import AbstractView
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util.data_loutr import NUMERICAL_VARIABLES, mean_hi_lo_over_years

# plot mean band time series
def get_time_series_fig(x_axis_name, y_axis_name, normalized_time_series, years):
    mean_std_time_series = mean_hi_lo_over_years(normalized_time_series.iloc[:, normalized_time_series.columns.get_level_values(level='Jahr').isin(years)])
    fig = make_subplots(rows=2, cols=1)

    x = list(mean_std_time_series.index)

    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[x_axis_name]['high']) + list(mean_std_time_series[x_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[y_axis_name]['high']) + list(mean_std_time_series[y_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name=y_axis_name,
        showlegend=False
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[x_axis_name]['mean'],
        line_color='rgb(0,100,80)',
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[y_axis_name]['mean'],
        line_color='rgb(0,176,246)',
        name=y_axis_name
    ), row=2, col=1)
    fig.update_traces(mode='lines')
    return fig


class ViewTimeSeries(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Time Series'
        self.value = self.label + '-graph'
        self.add_display_option('Upper plot', NUMERICAL_VARIABLES)
        self.add_display_option('Lower plot', NUMERICAL_VARIABLES, default_selection=1)

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        x_axis_name = kwargs[self.get_display_option_id('Upper plot')]
        y_axis_name = kwargs[self.get_display_option_id('Lower plot')]
        self.fig = get_time_series_fig(x_axis_name, y_axis_name, normalized_time_series, years)