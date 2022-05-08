from util.data_loutr import NUMERICAL_VARIABLES
from views.abstract_view import AbstractView
import plotly.express as px

class ViewHeatmap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Wärmebild'
        self.value = self.label + '-graph'
        self.add_display_option('x-Achse', NUMERICAL_VARIABLES)
        self.add_display_option('y-Achse', NUMERICAL_VARIABLES, default_selection=1)
        self.add_display_option('Mass', ['Dauer (min)', 'Anzahl'])

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        measure = kwargs[self.get_display_option_id('Mass')]
        x_axis_name = kwargs[self.get_display_option_id('x-Achse')]
        y_axis_name = kwargs[self.get_display_option_id('y-Achse')]
        df = opnrcd_df.copy()
        df[NUMERICAL_VARIABLES] = df[NUMERICAL_VARIABLES].astype("category")
        if x_axis_name == y_axis_name:
            df[x_axis_name+" "] = df[x_axis_name]
            heatmap_df = self.get_heatmap_df(df, measure, x_axis_name, x_axis_name+" ")
        else:
            heatmap_df = self.get_heatmap_df(df, measure, x_axis_name, y_axis_name)
        self.fig = px.imshow(heatmap_df, origin='lower')
        self.fig.update_layout(xaxis = {'dtick': 1})
        self.fig.update_layout(yaxis = {'dtick': 1})
        self.fig.data[0].hovertemplate = x_axis_name + ' = %{x}<br>' + y_axis_name + ' = %{y}<br>' + measure + ' = %{z}<extra></extra>'
        self.fig.update_layout(transition_duration=200)        

    def get_heatmap_df(self, df, measure, x_axis_name, y_axis_name):
        if measure == 'Anzahl':
            df = df.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)  # count
        else:
            df = df.groupby([x_axis_name, y_axis_name]).sum()['Dauer (m)'].unstack(x_axis_name).fillna(0.0)  # duration
        return df
