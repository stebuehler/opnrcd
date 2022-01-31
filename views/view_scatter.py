from views.abstract_view import AbstractView
from util.filter import Filter
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewScatter(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Scatter'
        self.value = self.label + '-graph'
        self.active_filters = ['x-axis' + self.label, 'y-axis' + self.label, 'Group by' + self.label, 'Color' + self.label]
        self.display_options = [
            Filter('x-axis' + self.label, NUMERICAL_VARIABLES + ['Timestamp sekunden']),
            Filter('y-axis' + self.label, NUMERICAL_VARIABLES + ['Timestamp sekunden'], default_selection=1),
            Filter('Group by' + self.label, ['Jahr', 'Nationalität', 'Sprache', 'Baujahr', 'Künstler', 'Titel']),
            Filter('Color' + self.label, NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Jahr', 'Baujahr'], default_selection=2),
        ]

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        years = kwargs['Jahre']
        x_axis_name = kwargs['x-axis' + self.label]
        y_axis_name = kwargs['y-axis' + self.label]
        color = kwargs['Color' + self.label]
        groupby = kwargs['Group by' + self.label]
        df = self.get_df(opnrcd_df, x_axis_name, y_axis_name, color, groupby, years)
        self.fig = px.scatter(
            df,
            x=x_axis_name,
            y=y_axis_name,
            color=color,
            size='Dauer (m)',
            text=self.show_labels_depending_on(groupby),
            hover_data=[groupby]
            )
        self.fig.update_traces(textposition='top center')
        self.fig.update_layout(transition_duration=200)

    def get_df(self, opnrcd_df, x_axis_name, y_axis_name, color, groupby, years):
        df = opnrcd_df[opnrcd_df['Jahr'].isin(years)]
        df = df.astype({'Jahr': 'int64'})
        df['aux_x'] = df[x_axis_name]*df['Dauer (m)']
        df['aux_y'] = df[y_axis_name]*df['Dauer (m)']
        df['aux_color'] = df[color]*df['Dauer (m)']
        df = df.groupby([groupby]).agg(
            aux_x=('aux_x', "sum"),
            aux_y=('aux_y', "sum"),
            aux_color=('aux_color', "sum"),
            dauer=('Dauer (m)', "sum")
            ).reset_index()
        df[x_axis_name] = df['aux_x']/df['dauer']
        df[y_axis_name] = df['aux_y']/df['dauer']
        df[color] = df['aux_color']/df['dauer']
        df['Dauer (m)'] = df['dauer']
        return df

    def show_labels_depending_on(self, groupby):
        if groupby == "Künstler" or groupby == "Titel":
            return None
        else:
            return groupby