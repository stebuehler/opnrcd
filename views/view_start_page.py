from views.abstract_view import AbstractView
from dash import Output
from util.data_loutr import NUMERICAL_VARIABLES, get_all_entries_for_column
import dash_bootstrap_components as dbc
from dash import html
from math import floor
from random import random

class ViewStartPage(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Strophensteckbrief'
        self.value = self.label + '-graph'
        self.starting_page = True
        self.add_display_option('Strophe', [])
        self.add_pre_display_option('Zufallsstrophe', button=True, button_text="Ich glaub ich hab Glück!")
        self.define_pre_display_target_outputs()

    def define_pre_display_target_outputs(self):
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Strophe') + '-select', 'options'))
        self.pre_display_option_target_outputs.append(Output(self.get_display_option_id('Strophe') + '-select', 'value'))

    def apply_pre_display_options(self, df, **kwargs):
        entries = get_all_entries_for_column('Strophentitel', df)
        return_dict = [{'label': i, 'value': i} for i in entries]
        random_index = floor(random()*len(entries))
        return [return_dict, entries[random_index]] if len(entries) > 0 else [return_dict, None]

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        strophe = kwargs[self.get_display_option_id('Strophe')]
        df = opnrcd_df[opnrcd_df['Strophentitel'] == strophe]
        dauer = df["Dauer (s)"].iloc[0]
        dauer_string = f'{floor(dauer / 60):.0f}' + ':' + f'{dauer - 60*floor(dauer / 60):02d}'
        self.card = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H4(strophe, className='card-title'),
                    ]
                ),
                dbc.CardBody(
                    [
                        html.H5(df['Künstler'], className='card-subtitle', style={'margin-bottom': '0.3rem'}),
                        html.H6('OPNRCD ' + df['Jahr'], className='card-subtitle'),
                        html.P([
                            html.Br(),
                            'Nationalität Künstler:    ' + df["Nationalität"].iloc[0], html.Br(),
                            'Sprache:                  ' + df["Sprache"].iloc[0], html.Br(),
                            'Baujahr:                  ' + f'{df["Baujahr"].iloc[0]:.0f}', html.Br(),
                            html.Br(),
                            'Dauer:                    ' + dauer_string, html.Br(),
                            'Startzeit auf CD:         ' + df["Startzeit"].iloc[0], html.Br(),
                            'Startzeit normalisiert:   ' + f'{df["Startzeit normalisiert"].iloc[0]:.1%}', html.Br(),
                            html.Br(),
                            'Künstlerische Relevanz:   ' + f'{df["Künstlerische Relevanz"].iloc[0]:.0f}', html.Br(),
                            'Musikalische Härte:       ' + f'{df["Musikalische Härte"].iloc[0]:.0f}', html.Br(),
                            'Tanzbarkeit:              ' + f'{df["Tanzbarkeit"].iloc[0]:.0f}', html.Br(),
                            'Nervofantigkeit:          ' + f'{df["Nervofantigkeit"].iloc[0]:.0f}', html.Br(),
                            'Verblödungsfaktor:        ' + f'{df["Verblödungsfaktor"].iloc[0]:.0f}', html.Br(),
                            'Weirdness:                ' + f'{df["Weirdness"].iloc[0]:.0f}',
                        ],
                        className='card-text',
                        style={'white-space': 'pre', 'font-family': 'monospace'},
                        ),
                    ]
                ),
            ],
            outline=True,
            color='dark',
        )
