from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewTreemap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Kacheldiagramm'
        self.value = self.label + '-graph'
        self.add_display_option('Mass', ['Dauer (min)', 'Anzahl'])
        self.add_display_option('Gruppierung', ['Jahr', 'Nationalität', 'Sprache', 'Baujahr', 'Künstler', 'Strophentitel'])
        self.add_display_option('Farbe', NUMERICAL_VARIABLES + ['Startzeit (s)', 'Jahr', 'Baujahr'], default_selection=2)

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        measure = kwargs[self.get_display_option_id('Mass')]
        color=kwargs[self.get_display_option_id('Farbe')]
        df = self.prepare_df(opnrcd_df)
        treemap_path = self.give_path(kwargs[self.get_display_option_id('Gruppierung')])
        self.fig = px.treemap(
            df, path=treemap_path, 
            values='Anzahl' if measure == 'Anzahl' else 'Dauer (m)',
            color=color,
            )
        self.fig.update(layout_showlegend=False)
        self.fig.data[0].hovertemplate = '<b>%{label}</b><br>' + measure + ' = %{value}<br>' + color + ' = %{color:.2f}<extra></extra>'

    def prepare_df(self, df):
        df['Total'] = 'Total'
        df['Anzahl'] = 1
        df = df.astype({'Jahr': 'int64'})
        return df

    def give_path(self, groupby):
        if groupby == 'Nationalität':
            return ['Total', 'Kontinent', 'Nationalität', 'Künstler', 'Strophentitel']
        elif groupby == 'Sprache':
            return ['Total', 'Sprache gruppiert 2', 'Sprache', 'Künstler', 'Strophentitel']
        elif groupby == 'Baujahr':
            return ['Total', 'Baujahr Jahrzehnt', 'Baujahr', 'Künstler', 'Strophentitel']
        elif groupby == 'Jahr':
            return ['Total', 'Jahr', 'Künstler', 'Strophentitel']
        elif groupby == 'Künstler':
            return ['Total', 'Künstler', 'Strophentitel']
        elif groupby == 'Strophentitel':
            return ['Total', 'Strophentitel']
        else:
            raise NotImplementedError