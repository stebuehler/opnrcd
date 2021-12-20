import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util.data_loutr import NUMERICAL_VARIABLES, mean_hi_lo_over_years


# plot mean band time series
def get_time_series_fig(x_axis_name, y_axis_name, normalized_time_series, years):
    mean_std_time_series = mean_hi_lo_over_years(normalized_time_series.iloc[:, normalized_time_series.columns.get_level_values(level='Jahr').isin(years)])
    fig = make_subplots(rows=2, cols=1)

    x = list(mean_std_time_series.index)

    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[x_axis_name]['high']) + list(mean_std_time_series[x_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x+x[::-1],
        y=list(mean_std_time_series[y_axis_name]['high']) + list(mean_std_time_series[y_axis_name]['low'])[::-1],
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name=y_axis_name,
        showlegend=False
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[x_axis_name]['mean'],
        line_color='rgb(0,100,80)',
        name=x_axis_name
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x, y=mean_std_time_series[y_axis_name]['mean'],
        line_color='rgb(0,176,246)',
        name=y_axis_name
    ), row=2, col=1)
    fig.update_traces(mode='lines')
    return fig


# For now the active filters are defined staticly
active_filter_dict = {
    'Scatter':  ['Block', 'Block', 'Block', 'None'], 
    'Heatmap': ['Block', 'Block', 'Block', 'Block'], 
    'Correlation': ['None', 'None', 'Block', 'None'], 
    'Time Series': ['Block', 'Block', 'Block', 'None'],
    'Treemap': ['Block', 'Block', 'None', 'Block']
}

class View:
    def __init__(self, label, value):
        self.label = label
        self.value = value
        # Note that for each filter we need the same display-style dictionary twice, once for the label and once for the filter
        self.active_filters = [item for sublist in [[{'display': style}]*2 for style in active_filter_dict[self.label]] for item in sublist]

    # When the logic per tab gets too complicated, we should refactor this to one file per tab and define fig per tab there
    def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
        df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        if self.value == 'tab-1-graph':
            self.fig = px.scatter(df, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr')
            self.fig.update_layout(transition_duration=200)
        elif self.value == 'tab-2-graph':
            if measure == 'Count':
                heatmap_df = df.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)  # count
            else:
                heatmap_df = df.groupby([x_axis_name, y_axis_name]).sum()['Dauer (s)'].unstack(x_axis_name).fillna(0.0)  # duration
            self.fig = px.imshow(heatmap_df)
            self.fig.update_layout(transition_duration=200)
        elif self.value == 'tab-3-graph':
            corr_df = df[NUMERICAL_VARIABLES].dropna().corr()
            self.fig = px.imshow(corr_df)
            # TODO find a way to show correlation numbers in heat map
            # fig.update_traces(textposition='inside')
            self.fig.update_layout(transition_duration=200)
        elif self.value == 'tab-4-graph':
            self.fig = get_time_series_fig(x_axis_name, y_axis_name, normalized_time_series, years)
        elif self.value == 'tab-5-graph':
            # TODO Let user chose if grouping by Country or different attribute (Baujahr etc.)
            # TODO choice whether to include skits or not (currently not)
            df['Planet'] = 'Welt'
            df['Count'] = 1
            self.fig = px.treemap(df, path=['Planet', 'Kontinent', 'Nationalität', 'Künstler', 'Titel'], values='Count' if measure == 'Count' else 'Dauer (s)')
            self.fig.data[0].hovertemplate = '%{label}<br>%{value}'

    def get_div(self):
        return html.Div([dcc.Graph(id=self.label, figure=self.fig)]), *self.active_filters

    def get_tab(self):
        return dcc.Tab(label=self.label, value=self.value)
