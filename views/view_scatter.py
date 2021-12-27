from views.abstract_view import AbstractView
import plotly.express as px

ACTIVE_FILTER_LIST = ['Block', 'Block', 'Block', 'None']

class ViewScatter(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Scatter'
        self.value = self.label + '-graph'
        self.active_filters = [item for sublist in [[{'display': style}]*2 for style in ACTIVE_FILTER_LIST] for item in sublist]

    def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        self.fig = px.scatter(self.df, x=x_axis_name, y=y_axis_name, size='Dauer (s)', color='Jahr')
        self.fig.update_layout(transition_duration=200)