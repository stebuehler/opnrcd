from views.abstract_view import AbstractView
import plotly.express as px

from util.data_loutr import NUMERICAL_VARIABLES

ACTIVE_FILTER_LIST = ['None', 'None', 'Block', 'None']

class ViewCorrelation(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Correlation'
        self.value = self.label + '-graph'
        self.active_filters = [item for sublist in [[{'display': style}]*2 for style in ACTIVE_FILTER_LIST] for item in sublist]

    def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
        self.df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]  
        corr_df = self.df[NUMERICAL_VARIABLES].dropna().corr()
        self.fig = px.imshow(corr_df)
        # TODO find a way to show correlation numbers in heat map
        # fig.update_traces(textposition='inside')
        self.fig.update_layout(transition_duration=200)