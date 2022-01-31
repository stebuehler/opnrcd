from util.data_loutr import NUMERICAL_VARIABLES
from util.filter import Filter
from views.abstract_view import AbstractView
import plotly.express as px

class ViewHeatmap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Heatmap'
        self.value = self.label + '-graph'
        self.active_filters = ['x-axis' + self.label, 'y-axis' + self.label, 'Measure' + self.label]
        self.display_options = [
            Filter('x-axis' + self.label, NUMERICAL_VARIABLES),
            Filter('y-axis' + self.label, NUMERICAL_VARIABLES, default_selection=1),
            Filter('Measure' + self.label, ['Dauer (min)', 'Count']),
        ]

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        measure = kwargs['Measure' + self.label]
        x_axis_name = kwargs['x-axis' + self.label]
        y_axis_name = kwargs['y-axis' + self.label]
        df = opnrcd_df.copy()
        df[NUMERICAL_VARIABLES] = df[NUMERICAL_VARIABLES].astype("category")
        df = df[df['Jahr'].isin(years)]
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
