from views.abstract_view import AbstractView
import plotly.express as px
import numpy as np

from util.data_loutr import NUMERICAL_VARIABLES

class ViewCorrelation(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Korrelation'
        self.value = self.label + '-graph'

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        corr_df = self.prepare_df(opnrcd_df)
        self.fig = px.imshow(corr_df, text_auto=".2f", color_continuous_scale=px.colors.diverging.RdBu, color_continuous_midpoint=0)
        self.fig.update_layout(transition_duration=200)
        self.fig.data[0].hovertemplate = 'x: %{x}<br>y: %{y}<br>Korrelation = %{z:.3f}<extra></extra>'

    def prepare_df(self, df):
        df = df[NUMERICAL_VARIABLES + ['Dauer (m)', 'Baujahr', 'Timestamp sekunden']].dropna().corr()
        np.fill_diagonal(df.values, 0)
        return df