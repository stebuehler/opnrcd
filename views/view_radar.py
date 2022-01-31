from views.abstract_view import AbstractView
from util.filter import Filter
import plotly.express as px
import plotly.graph_objects as go
from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column

class ViewRadar(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Radar'
        self.value = self.label + '-graph'
        self.active_filters = ['Blau' + self.label, 'Rot' + self.label]
        alle_kuenstler = get_all_entries_for_column('Künstler')
        self.display_options = [
            Filter('Blau' + self.label, alle_kuenstler),
            Filter('Rot' + self.label, alle_kuenstler, default_selection=1),
        ]

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        sprachen = kwargs['Sprachen']
        radar1 = kwargs['Blau' + self.label]
        radar2 = kwargs['Rot' + self.label]
        df1 = self.prepare_df(opnrcd_df, years, sprachen, radar1)
        df2 = self.prepare_df(opnrcd_df, years, sprachen, radar2)
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatterpolar(
            r=df1['value'],
            theta=df1['index'],
            fill='toself',
            name=radar1,
            hoverinfo='r+name'
            ))
        self.fig.add_trace(go.Scatterpolar(
            r=df2['value'],
            theta=df2['index'],
            fill='toself',
            name=radar2,
            hoverinfo='r+name'
            ))
        self.fig.update_layout(polar=dict(radialaxis=dict(visible=True)),showlegend=False)

    def prepare_df(self, opnrcd_df, years, sprachen, filter):
        df =  opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        df =  df[df['Sprache'].isin(sprachen)]
        df = df[df['Künstler'].isin([filter])]
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
