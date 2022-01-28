from views.abstract_view import AbstractView
import plotly.express as px
import plotly.graph_objects as go
from util.data_loutr import NUMERICAL_VARIABLES

class ViewRadar(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Radar'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre', 'Sprachen']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        sprachen = kwargs['Sprachen']
        df = self.prepare_df(opnrcd_df, years, sprachen)
        self.fig = go.Figure(data=go.Scatterpolar(
            r=df['value'],
            theta=df['index'],
            fill='toself'
            ))

    def prepare_df(self, opnrcd_df, years, sprachen):
        df =  opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        df =  df[df['Sprache'].isin(sprachen)]
        dauer = 'Dauer (s)'
        df = df[NUMERICAL_VARIABLES + [dauer]]
        df['measure'] = 'value'
        for variable in NUMERICAL_VARIABLES:
            df[variable] = df[variable]*df[dauer]
        df = df.groupby(['measure']).mean()
        for variable in NUMERICAL_VARIABLES:
            df[variable] = df[variable]/df[dauer]
        df = df[NUMERICAL_VARIABLES].transpose().reset_index()
        return df
