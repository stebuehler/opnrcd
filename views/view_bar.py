from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewBar(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Balkendiagramm'
        self.value = self.label + '-graph'
        self.add_display_option('Gruppierung', ['Nationalität', 'Kontinent', 'Sprache', 'Baujahr', 'Baujahr Jahrzehnt'])
        # self.add_display_option('x-Achse', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)'])
        # self.add_display_option('y-Achse', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)'], default_selection=1)
        # self.add_display_option('Farbe', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)', 'Jahr', 'Baujahr'], default_selection=2)
        self.add_display_option('Beschriftung', ['An', 'Aus'], toggle=True)

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        # retrieve display options
        groupby = kwargs[self.get_display_option_id('Gruppierung')]
        # labels = groupby if kwargs[self.get_display_option_id('Beschriftung')] == 'An' else None
        df = self.get_df(opnrcd_df, groupby)
        self.fig = px.histogram(
            df,
            x='Jahr',
            y='Dauer (m)',
            color=groupby,
            #text_auto=True,
            #hover_name=groupby,
            )
        self.fig.update_layout(transition_duration=200)

    def get_df(self, df, groupby):
        df = df.sort_values(by=['Jahr'])
        return df