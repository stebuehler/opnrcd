from views.abstract_view import AbstractView
import plotly.express as px

class ViewTreemap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Treemap'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre', 'Measure', 'Group by', 'Color']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        measure = kwargs['Measure']
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        # TODO Let user chose if grouping by Country or different attribute (Baujahr etc.)
        self.df['All'] = 'All'
        self.df['Count'] = 1
        treemap_path = self.give_path(kwargs['Group by'])
        self.fig = px.treemap(
            self.df, path=treemap_path, 
            values='Count' if measure == 'Count' else 'Dauer (m)',
            color=kwargs['Color']
            )
        self.fig.data[0].hovertemplate = '<b>%{label}</b><br>Measure = %{value}<br>Color = %{color:.2f}'

    def give_path(self, groupby):
        if groupby == 'Nationalität':
            return ['All', 'Kontinent', 'Nationalität', 'Künstler', 'Titel']
        elif groupby == 'Sprache':
            return ['All', 'Sprache gruppiert 2', 'Sprache', 'Künstler', 'Titel']
        elif groupby == 'Baujahr':
            return ['All', 'Baujahr Jahrzehnt', 'Baujahr', 'Künstler', 'Titel']
        else:
            raise NotImplementedError