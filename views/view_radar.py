from views.abstract_view import AbstractView
from dash import Output
import plotly.express as px
import plotly.graph_objects as go
from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column

class ViewRadar(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Radar'
        self.value = self.label + '-graph'
        self.active_filters = ['Blau' + self.label, 'Rot' + self.label]
        self.add_display_option('Blau', [], color='blue')
        self.add_display_option('Rot', [], color='red')
        self.add_pre_display_option('Zu vergleichendes Attribut', ['Strophentitel', 'Künstler', 'Nationalität', 'Kontinent', 'Sprache', 'Baujahr', 'Baujahr Jahrzehnt', 'Jahr'])
        self.define_pre_display_target_outputs()

    def define_pre_display_target_outputs(self):
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Blau') + '-select', 'options'))
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Rot') + '-select', 'options'))
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Blau') + '-select', 'value'))
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Rot') + '-select', 'value'))

    def apply_pre_display_options(self, df, **kwargs):
        column = kwargs[self.get_pre_display_option_id('Zu vergleichendes Attribut')]
        entries = get_all_entries_for_column(column, df)
        return_dict = [{'label': i, 'value': i} for i in entries]
        if len(entries) > 0:
            return [return_dict, return_dict, entries[0], entries[1] if len(entries) > 1 else entries[0]]
        else:
            return [return_dict, return_dict, None, None]

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        column_chosen = kwargs[self.get_pre_display_option_id('Zu vergleichendes Attribut')]
        radar1 = kwargs[self.get_display_option_id('Blau')]
        radar2 = kwargs[self.get_display_option_id('Rot')]
        df1 = self.prepare_df(opnrcd_df, column_chosen, radar1)
        df2 = self.prepare_df(opnrcd_df, column_chosen, radar2)
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

    def prepare_df(self, df, filter_column, filter_value):
        df = df[df[filter_column].isin([filter_value])]
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
