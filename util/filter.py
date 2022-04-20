from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc

class Filter:
    def __init__(self, label, options=None, tab_name=None, column_name=None, default_selection: int=0, multi: bool=False, clearable: bool=True, color=None, toggle: bool=False, button: bool=False, button_text=None, range_slider: bool=False, range=None, step=None):
        self.name = label + "-" + tab_name if tab_name is not None else column_name if column_name is not None else label
        self.label = html.Label([f'{label}:'], style={'font-weight': 'bold', 'text-align': "left", 'color': color}, id=f'{self.name}-select-label')
        self.color = color
        self.is_multi = multi
        self.is_toggle = toggle
        self.is_button = button
        self.is_range_slider = range_slider
        default_selection = None if options is None else options if multi else options[default_selection] if len(options)>0 else None
        if self.is_toggle:
            self.toggle = dcc.RadioItems(
                id=f'{self.name}-select',
                options=[{'label': i, 'value': i} for i in options],
                value=default_selection,
                inputStyle={'margin-right': '5px', 'margin-left': '5px'}
                )
        elif self.is_button:
            self.button = dbc.Button(
                button_text if button_text is not None else label,  
                id=f'{self.name}-select',
                color="primary",
                n_clicks=0,
                )
        elif self.is_range_slider:
            self.range_slider = dcc.RangeSlider(
                range[0],
                range[1],
                step,
                value=range,
                id=f'{self.name}-select',
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
        elif self.is_button:
            return self.get_label_dropdown_button()
        elif self.is_range_slider:
            return self.get_label_dropdown_range_slider()
        else:
            return self.get_label_dropdown_single()
    
    def get_label_dropdown_single(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label], id=f'{self.name}-select-label-div')]),
            dbc.Row([html.Div([self.dropdown], id=f'{self.name}-select-div')]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_label_dropdown_multi(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label], id=f'{self.name}-select-label-div')]),
            dbc.Row([html.Div([self.dropdown], id=f'{self.name}-select-div')]),
        ]
        , width=12)

    def get_label_dropdown_toggle(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label], id=f'{self.name}-select-label-div')]),
            dbc.Row([html.Div([self.toggle], id=f'{self.name}-select-div')]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_label_dropdown_button(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label], id=f'{self.name}-select-label-div')]),
            dbc.Row([html.Div([self.button], id=f'{self.name}-select-div')]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_label_dropdown_range_slider(self):
        return dbc.Col([
            dbc.Row([html.Div([self.label], id=f'{self.name}-select-label-div')]),
            dbc.Row([html.Div([self.range_slider], id=f'{self.name}-select-div')]),
        ]
        , width=3, xs=6, sm=6, md=4, lg=3, xl=3)

    def get_input(self):
        if self.is_button:
            return Input(f'{self.name}-select', 'n_clicks')
        else:
            return Input(f'{self.name}-select', 'value')

    def get_output(self):
        return [Output(f'{self.name}-select-div', 'style'), Output(f'{self.name}-select-label-div', 'style')]
