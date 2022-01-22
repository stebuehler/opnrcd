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
        self.prepare_df(opnrcd_df, years)
        treemap_path = self.give_path(kwargs['Group by'])
        self.fig = px.treemap(
            self.df, path=treemap_path, 
            values='Count' if measure == 'Count' else 'Dauer (m)',
            color=kwargs['Color']
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