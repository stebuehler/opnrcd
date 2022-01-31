from views.abstract_view import AbstractView
from util.filter import Filter
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewTreemap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Treemap'
        self.value = self.label + '-graph'
        self.active_filters = ['Measure' + self.label, 'Group by' + self.label, 'Color' + self.label]
        self.display_options = [
            Filter('Measure' + self.label, ['Dauer (min)', 'Count']),
            Filter('Group by' + self.label, ['Jahr', 'Nationalität', 'Sprache', 'Baujahr', 'Künstler', 'Titel']),
            Filter('Color' + self.label, NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Jahr', 'Baujahr'], default_selection=2),
        ]

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        measure = kwargs['Measure' + self.label]
        self.prepare_df(opnrcd_df, years)
        treemap_path = self.give_path(kwargs['Group by' + self.label])
        self.fig = px.treemap(
            self.df, path=treemap_path, 
            values='Count' if measure == 'Count' else 'Dauer (m)',
            color=kwargs['Color' + self.label]
            )
        self.fig.update(layout_showlegend=False)
        self.fig.data[0].hovertemplate = '<b>%{label}</b><br>Measure = %{value}<br>Color = %{color:.2f}'

    def prepare_df(self, opnrcd_df, years):
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        self.df['All'] = 'All'
        self.df['Count'] = 1
        self.df = self.df.astype({'Jahr': 'int64'})

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