from views.abstract_view import AbstractView
import plotly.express as px
from util.data_loutr import NUMERICAL_VARIABLES

class ViewParallelCategory(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Parallel Category'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre', 'Sprachen']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        sprachen = kwargs['Sprachen']
        df = self.prepare_df(opnrcd_df, years, sprachen)
        self.fig = px.parallel_categories(
            df,
            dimensions=NUMERICAL_VARIABLES
            )

    def prepare_df(self, opnrcd_df, years, sprachen):
        df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        df = df[df['Sprache'].isin(sprachen)]
        return df