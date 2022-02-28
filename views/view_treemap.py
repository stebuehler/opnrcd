from views.abstract_view import AbstractView
from util.filter import Filter
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewTreemap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Kacheldiagramm'
        self.value = self.label + '-graph'
        self.add_display_option('Mass', ['Dauer (min)', 'Anzahl'])
        self.add_display_option('Gruppierung', ['Jahr', 'Nationalität', 'Sprache', 'Baujahr', 'Künstler', 'Titel'])
        self.add_display_option('Farbe', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Jahr', 'Baujahr'], default_selection=2)

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        measure = kwargs[self.get_display_option_id('Mass')]
        df = self.prepare_df(opnrcd_df)
        treemap_path = self.give_path(kwargs[self.get_display_option_id('Gruppierung')])
        self.fig = px.treemap(
            df, path=treemap_path, 
            values='Count' if measure == 'Anzahl' else 'Dauer (m)',
            color=kwargs[self.get_display_option_id('Farbe')]
            )
        self.fig.update(layout_showlegend=False)
        self.fig.data[0].hovertemplate = '<b>%{label}</b><br>Mass = %{value}<br>Farbe = %{color:.2f}'

    def prepare_df(self, df):
        df['All'] = 'All'
        df['Count'] = 1
        df = df.astype({'Jahr': 'int64'})
        return df

    def give_path(self, groupby):
        if groupby == 'Nationalität':
            return ['All', 'Kontinent', 'Nationalität', 'Künstler', 'Titel']
        elif groupby == 'Sprache':
            return ['All', 'Sprache gruppiert 2', 'Sprache', 'Künstler', 'Titel']
        elif groupby == 'Baujahr':
            return ['All', 'Baujahr Jahrzehnt', 'Baujahr', 'Künstler', 'Titel']
        elif groupby == 'Jahr':
            return ['All', 'Jahr', 'Künstler', 'Titel']
        elif groupby == 'Künstler':
            return ['All', 'Künstler', 'Titel']
        elif groupby == 'Titel':
            return ['All', 'Titel']
        else:
            raise NotImplementedError