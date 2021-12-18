from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

class Filter:
    def __init__(self, name, options, default_selection: int=0, multi: bool=False):
        self.name = name
        self.options = options
        self.multi = multi
        self.default_selection = self.options if multi else self.options[default_selection]
        self.label = html.Label([f'{self.name}:'], style={'font-weight': 'bold', "text-align": "left"}, id=f'{self.name}-select-label')
        self.dropdown = dcc.Dropdown(
            id=f'{self.name}-select', options=[{'label': i, 'value': i} for i in self.options],
            multi=self.multi, value=self.default_selection
        )

    def get_label_dropdown(self):
        return [self.label, self.dropdown]

    def get_input(self):
        return Input(f'{self.name}-select', 'value')

    def get_output(self):
        return [Output(f'{self.name}-select', 'style'), Output(f'{self.name}-select-label', 'style')]
