from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewScatter(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Streudiagramm'
        self.value = self.label + '-graph'
        self.add_display_option('Group by', ['Jahr', 'Nationalität', 'Kontinent', 'Sprache', 'Baujahr', 'Baujahr Jahrzehnt', 'Künstler', 'Titel'])
        self.add_display_option('x-axis', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)'])
        self.add_display_option('y-axis', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)'], default_selection=1)
        self.add_display_option('Color', NUMERICAL_VARIABLES + ['Timestamp sekunden', 'Dauer (m)', 'Jahr', 'Baujahr'], default_selection=2)

    def generate_fig(self, opnrcd_df, normalized_time_series, **kwargs):
        # retrieve display options
        x_axis_name = kwargs[self.get_display_option_id('x-axis')]
        y_axis_name = kwargs[self.get_display_option_id('y-axis')]
        color = kwargs[self.get_display_option_id('Color')]
        groupby = kwargs[self.get_display_option_id('Group by')]
        df = self.get_df(opnrcd_df, x_axis_name, y_axis_name, color, groupby)
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

    def get_df(self, df, x_axis_name, y_axis_name, color, groupby):
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