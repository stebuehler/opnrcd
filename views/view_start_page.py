from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column
import dash_bootstrap_components as dbc
from dash import html

class ViewStartPage(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Strophenansicht'
        self.value = self.label + '-graph'
        self.starting_page = True
        self.add_display_option('Strophe', get_all_entries_for_column('Titel'))

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        strophe = kwargs[self.get_display_option_id('Strophe')]
        df = opnrcd_df[opnrcd_df['Titel'] == strophe]
        self.card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(df["Künstler"] + " - " + strophe, className="card-title"),
                    html.H5("OPNRCD " + df["Jahr"], className="card-subtitle"),
                    html.P("Künstlerische Relevanz: " + f'{df["Künstlerische Relevanz (1-10)"].iloc[0]:.0f}', className="card-text",),
                ]
            ),
        )
