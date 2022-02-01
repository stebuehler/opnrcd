from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc

class Filter:
    def __init__(self, label, options, tab_name=None, default_selection: int=0, multi: bool=False, clearable: bool=True):
        self.name = label + "-" + tab_name if tab_name is not None else label
        self.options = options
        self.multi = multi
        self.clearable = clearable
        self.default_selection = self.options if multi else self.options[default_selection]
        self.label = html.Label([f'{label}:'], style={'font-weight': 'bold', "text-align": "left"}, id=f'{self.name}-select-label')
        self.dropdown = dcc.Dropdown(
            id=f'{self.name}-select', options=[{'label': i, 'value': i} for i in self.options],
            multi=self.multi, value=self.default_selection, clearable=self.clearable
        )

    def get_label_dropdown(self):
        if self.multi:
            return self.get_label_dropdown_multi()
        else:
            return self.get_label_dropdown_single()
    
    def get_label_dropdown_single(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label])]),
            dbc.Row([html.Div([self.dropdown])]),
        ]
        , width=2, xs=6, sm=6, md=4, lg=2, xl=2, className="g-0")

    def get_label_dropdown_multi(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label])]),
            dbc.Row([html.Div([self.dropdown])]),
        ]
        , width=12, className="g-0")

    def get_input(self):
        return Input(f'{self.name}-select', 'value')

    def get_output(self):
        return [Output(f'{self.name}-select', 'style'), Output(f'{self.name}-select-label', 'style')]
