from util.data_loutr import NUMERICAL_VARIABLES
from views.abstract_view import AbstractView
import plotly.express as px

class ViewHeatmap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Wärmebild'
        self.value = self.label + '-graph'
        self.add_display_option('x-axis', NUMERICAL_VARIABLES)
        self.add_display_option('y-axis', NUMERICAL_VARIABLES, default_selection=1)
        self.add_display_option('Measure', ['Dauer (min)', 'Count'])

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        measure = kwargs[self.get_display_option_id('Measure')]
        x_axis_name = kwargs[self.get_display_option_id('x-axis')]
        y_axis_name = kwargs[self.get_display_option_id('y-axis')]
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
        self.fig.update_layout(transition_duration=200)        

    def get_heatmap_df(self, df, measure, x_axis_name, y_axis_name):
        if measure == 'Count':
            df = df.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)  # count
        else:
            df = df.groupby([x_axis_name, y_axis_name]).sum()['Dauer (m)'].unstack(x_axis_name).fillna(0.0)  # duration
        return df
