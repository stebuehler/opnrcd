from views.abstract_view import AbstractView
import plotly.express as px

class ViewScatter(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Scatter'
        self.value = self.label + '-graph'
        self.active_filters = ['x-axis', 'y-axis', 'Jahre']

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        x_axis_name = kwargs['x-axis']
        y_axis_name = kwargs['y-axis']
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        self.fig = px.scatter(self.df, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr', hover_data=['Künstler', 'Titel'])
        self.fig.update_layout(transition_duration=200)