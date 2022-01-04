from views.abstract_view import AbstractView
import plotly.express as px

class ViewTreemap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Treemap'
        self.value = self.label + '-graph'
        self.active_filters = ['Jahre', 'Measure']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        measure = kwargs['Measure']
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        # TODO Let user chose if grouping by Country or different attribute (Baujahr etc.)
        # TODO choice whether to include skits or not (currently not)
        self.df['Planet'] = 'Welt'
        self.df['Count'] = 1
        self.fig = px.treemap(self.df, path=['Planet', 'Kontinent', 'Nationalität', 'Künstler', 'Titel'], values='Count' if measure == 'Count' else 'Dauer (s)')
        self.fig.data[0].hovertemplate = '%{label}<br>%{value}'