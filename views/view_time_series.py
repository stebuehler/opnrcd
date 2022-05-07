from views.abstract_view import AbstractView
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util.data_loutr import NUMERICAL_VARIABLES, mean_hi_lo_over_years

# plot mean band time series
def get_time_series_fig(x_axis_name, y_axis_name, mean_std_time_series, single_year=None):
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
        name=x_axis_name,
        hovertemplate='x = %{x:.2f}<br>y = %{y:.2f}<br>',
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[y_axis_name]['mean'],
        line_color='rgb(0,176,246)',
        name=y_axis_name,
        hovertemplate='x = %{x:.2f}<br>y = %{y:.2f}<br>',
    ), row=2, col=1)
    if single_year:
        print(mean_std_time_series)
        fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[x_axis_name]['mean'],
        line_color='rgb(100,0,0)',
        name=single_year,
        hovertemplate='x = %{x:.2f}<br>y = %{y:.2f}<br>',
        ), row=1, col=1)
    fig.update_traces(mode='lines')
    return fig


class ViewTimeSeries(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Zeitreihe'
        self.value = self.label + '-graph'
        self.add_display_option('Obere Kurve', NUMERICAL_VARIABLES)
        self.add_display_option('Untere Kurve', NUMERICAL_VARIABLES, default_selection=1)
        self.add_display_option('Einzelnes Jahr', ['2020', '2021'])
        self.hide_filters_other_than_year = True

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        x_axis_name = kwargs[self.get_display_option_id('Obere Kurve')]
        y_axis_name = kwargs[self.get_display_option_id('Untere Kurve')]
        single_year = kwargs[self.get_display_option_id('Einzelnes Jahr')]
        self.fig = get_time_series_fig(x_axis_name, y_axis_name, normalized_time_series, single_year)