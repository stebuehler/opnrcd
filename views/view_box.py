from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px
import pandas as pd

class ViewBox(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Kastengrafik'
        self.value = self.label + '-graph'
        self.add_display_option('x-Achse', ['Jahr', 'Kontinent', 'Sprache gruppiert', 'Baujahr Jahrzehnt', 'Nationalität', 'Bewertungskategorien'])
        self.add_display_option('y-Achse', NUMERICAL_VARIABLES + ['Startzeit normalisiert', 'Dauer (m)', 'Jahr', 'Baujahr (<1950 in 1950 enthalten)'])
        self.add_display_option('Alle Punkte anzeigen', ['An', 'Aus'], toggle=True, default_selection=1)

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        # retrieve display options
        x_axis_name = kwargs[self.get_display_option_id('x-Achse')]
        y_axis_name = kwargs[self.get_display_option_id('y-Achse')]
        y_axis_name = 'Baujahr mapped' if y_axis_name == 'Baujahr (<1950 in 1950 enthalten)' else y_axis_name
        points_bool = kwargs[self.get_display_option_id('Alle Punkte anzeigen')]
        points = 'all' if points_bool == 'An' else False
        # the case where all categories are shown at once needs to be treated separately
        categories_ax_x_axis = True if x_axis_name == 'Bewertungskategorien' else False
        if categories_ax_x_axis:
            x_axis_name = 'Bewertungskategorie'
            y_axis_name = 'Wert'
        df = self.get_df(opnrcd_df, pivot_for_numerical_variables=categories_ax_x_axis).sort_values(by=x_axis_name)
        self.fig = px.box(
            df,
            x=x_axis_name,
            y=y_axis_name,
            points=points,
            )
        self.fig.update_layout(transition_duration=200)

    def get_df(self, df, pivot_for_numerical_variables=False):
        if not pivot_for_numerical_variables:
            return df.astype({'Jahr': 'int64'})
        else:
            return pd.melt(
                df,
                id_vars=None,
                value_vars=NUMERICAL_VARIABLES,
                var_name='Bewertungskategorie',
                value_name='Wert'
                )
            