from views.abstract_view import AbstractView
from dash import Output
from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column
import dash_bootstrap_components as dbc
from dash import html

class ViewStartPage(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Strophenansicht'
        self.value = self.label + '-graph'
        self.starting_page = True
        self.add_display_option('Strophe', [])
        self.define_pre_display_target_outputs()

    def define_pre_display_target_outputs(self):
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Strophe') + '-select', 'options'))
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Strophe') + '-select', 'value'))

    def apply_pre_display_options(self, df, **kwargs):
        entries = get_all_entries_for_column("Titel", df)
        return_dict = [{'label': i, 'value': i} for i in entries]
        return [return_dict, entries[0]]

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        strophe = kwargs[self.get_display_option_id('Strophe')]
        df = opnrcd_df[opnrcd_df['Titel'] == strophe]
        self.card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(df["Künstler"] + " - " + strophe, className="card-title"),
                    html.H5("OPNRCD " + df["Jahr"], className="card-subtitle"),
                    html.P([
                        html.Br(),
                        "Künstlerische Relevanz:   " + f'{df["Künstlerische Relevanz (1-10)"].iloc[0]:.0f}', html.Br(),
                        "Musikalische Härte:         " + f'{df["Musikalische Härte (1-10)"].iloc[0]:.0f}', html.Br(),
                        "Tanzbarkeit:                     " + f'{df["Tanzbarkeit (1-10)"].iloc[0]:.0f}', html.Br(),
                        "Nervofantigkeit:              " + f'{df["Nervofantigkeit (1-10)"].iloc[0]:.0f}', html.Br(),
                        "Verblödungsfaktor:         " + f'{df["Verblödungsfaktor (1-10)"].iloc[0]:.0f}', html.Br(),
                        "Weirdness:                      " + f'{df["Weirdness (1-8)"].iloc[0]:.0f}',
                    ],
                     className="card-text",
                     style={'white-space': 'pre'},
                     ),
                ]
            ),
            # className="w-75 mb-3",
        )
