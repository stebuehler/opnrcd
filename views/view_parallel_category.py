from views.abstract_view import AbstractView
import plotly.express as px
from util.data_loutr import NUMERICAL_VARIABLES

class ViewParallelCategory(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Parallel Category'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre', 'Sprachen', 'Variables to show', 'Level of detail']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        sprachen = kwargs['Sprachen']
        variables_to_show = kwargs['Variables to show']
        grouped = kwargs['Level of detail'] == 'Reduced (Low-Mid-High)'
        df = self.prepare_df(opnrcd_df, years, sprachen, grouped)
        self.fig = px.parallel_categories(
            df,
            dimensions=variables_to_show,
            #color='Baujahr',
            )

    def prepare_df(self, opnrcd_df, years, sprachen, group=True):
        df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        df = df[df['Sprache'].isin(sprachen)]
        if group:
            df = self.group_numerical_variables(df)
        return df

    def group_numerical_variables(self, df):
        map_for_all_except_weirdness = {
            1: 'Low',
            2: 'Low',
            3: 'Low',
            4: 'Mid',
            5: 'Mid',
            6: 'Mid',
            7: 'Mid',
            8: 'High',
            9: 'High',
            10: 'High'
        }
        map_for_weirdness = {
            1: 'Low',
            2: 'Low',
            3: 'Mid',
            4: 'Mid',
            5: 'Mid',
            6: 'Mid',
            7: 'High',
            8: 'High',
        }
        for variable in NUMERICAL_VARIABLES:
            mapping = map_for_weirdness if variable == 'Weirdness' else map_for_all_except_weirdness
            df[variable] = df[variable].map(mapping)
        return df