from views.abstract_view import AbstractView
import plotly.express as px
import numpy as np

from util.data_loutr import NUMERICAL_VARIABLES

class ViewCorrelation(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Correlation'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        corr_df = self.prepare_df(opnrcd_df, years)
        self.fig = px.imshow(corr_df, text_auto=".2f", color_continuous_scale=px.colors.diverging.RdBu, color_continuous_midpoint=0)
        # TODO find a way to show correlation numbers in heat map
        # fig.update_traces(textposition='inside')
        # This here will work as soon as dash version > 2.0.0 is available that supports the plotly v 5.5.0 feature of the "text_auto" argument:
        # self.fig = px.imshow(corr_df, text_auto=".2f", color_continuous_scale=px.colors.diverging.RdBu, color_continuous_midpoint=0)
        # or we could place our own more up to date plotly.js file in the repo (in an "assets" folder) and refer to it.
        # https://stackoverflow.com/questions/70512660/how-to-show-text-on-a-heatmap-with-plotly/70516115
        # https://dash.plotly.com/external-resources
        self.fig.update_layout(transition_duration=200)

    def prepare_df(self, df, years):
        df = df[df['Jahr'].isin(years)]  
        df = df[NUMERICAL_VARIABLES + ['Dauer (m)', 'Baujahr', 'Timestamp sekunden']].dropna().corr()
        np.fill_diagonal(df.values, 0)
        return df