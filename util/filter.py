from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc

class Filter:
    def __init__(self, label, options, tab_name=None, column_name=None, default_selection: int=0, multi: bool=False, clearable: bool=True, color=None, toggle: bool=False):
        self.name = label + "-" + tab_name if tab_name is not None else column_name if column_name is not None else label
        self.label = html.Label([f'{label}:'], style={'font-weight': 'bold', 'text-align': "left", 'color': color}, id=f'{self.name}-select-label')
        self.color = color
        self.is_multi = multi
        self.is_toggle = toggle
        default_selection = options if multi else options[default_selection] if len(options)>0 else None
        if self.is_toggle:
            self.toggle = dcc.RadioItems(
                id=f'{self.name}-select',
                options=[{'label': i, 'value': i} for i in options],
                value=default_selection,
                inputStyle={'margin-right': '5px', 'margin-left': '5px'}
                )
        else:
            self.dropdown = dcc.Dropdown(
                id=f'{self.name}-select',
                options=[{'label': i, 'value': i} for i in options],
                multi=self.is_multi,
                value=default_selection,
                clearable=clearable
                )

    def get_label_dropdown(self):
        if self.is_multi:
            return self.get_label_dropdown_multi()
        elif self.is_toggle:
            return self.get_label_dropdown_toggle()
        else:
            return self.get_label_dropdown_single()
    
    def get_label_dropdown_single(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label])]),
            dbc.Row([html.Div([self.dropdown])]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_label_dropdown_multi(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label])]),
            dbc.Row([html.Div([self.dropdown])]),
        ]
        , width=12)

    def get_label_dropdown_toggle(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label])]),
            dbc.Row([html.Div([self.toggle])]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_input(self):
        return Input(f'{self.name}-select', 'value')

    def get_output(self):
        return [Output(f'{self.name}-select', 'style'), Output(f'{self.name}-select-label', 'style')]
