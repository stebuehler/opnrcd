from views.abstract_view import AbstractView
import plotly.express as px

class ViewHeatmap(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Heatmap'
        self.value = self.label + '-graph'
        self.active_filters = ['x-axis', 'y-axis', 'Jahre', 'Measure']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        measure = kwargs['Measure']
        x_axis_name = kwargs['x-axis']
        y_axis_name = kwargs['y-axis']
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        if measure == 'Count':
            heatmap_df = self.df.groupby([x_axis_name, y_axis_name]).count()['Jahr'].unstack(x_axis_name).fillna(0.0)  # count
        else:
            heatmap_df = self.df.groupby([x_axis_name, y_axis_name]).sum()['Dauer (s)'].unstack(x_axis_name).fillna(0.0)  # duration
        self.fig = px.imshow(heatmap_df)
        self.fig.update_layout(transition_duration=200)