from views.abstract_view import AbstractView
import plotly.express as px

from util.data_loutr import NUMERICAL_VARIABLES

class ViewCorrelation(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Correlation'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]  
        corr_df = self.df[NUMERICAL_VARIABLES].dropna().corr()
        self.fig = px.imshow(corr_df)
        # TODO find a way to show correlation numbers in heat map
        # fig.update_traces(textposition='inside')
        self.fig.update_layout(transition_duration=200)