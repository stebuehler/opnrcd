from views.abstract_view import AbstractView
from util.data_loutr import NUMERICAL_VARIABLES
import plotly.express as px

class ViewScatter(AbstractView):
    def __init__(self):
        AbstractView.__init__(self)
        self.label = 'Streudiagramm'
        self.value = self.label + '-graph'
        self.add_display_option('Gruppierung', ['Jahr', 'Nationalität', 'Kontinent', 'Sprache', 'Baujahr', 'Baujahr Jahrzehnt', 'Künstler', 'Strophentitel'])
        self.add_display_option('x-Achse', NUMERICAL_VARIABLES + ['Startzeit normalisiert', 'Dauer (m)', 'Jahr', 'Baujahr'])
        self.add_display_option('y-Achse', NUMERICAL_VARIABLES + ['Startzeit normalisiert', 'Dauer (m)', 'Jahr', 'Baujahr'], default_selection=1)
        self.add_display_option('Farbe', NUMERICAL_VARIABLES + ['Startzeit normalisiert', 'Dauer (m)', 'Jahr', 'Baujahr'], default_selection=2)
        self.add_display_option('Beschriftung', ['An', 'Aus'], toggle=True)

    def generate_fig(self, opnrcd_df, normalized_time_series, time_series_by_year, **kwargs):
        # retrieve display options
        x_axis_name = kwargs[self.get_display_option_id('x-Achse')]
        y_axis_name = kwargs[self.get_display_option_id('y-Achse')]
        color = kwargs[self.get_display_option_id('Farbe')]
        groupby = kwargs[self.get_display_option_id('Gruppierung')]
        labels = groupby if kwargs[self.get_display_option_id('Beschriftung')] == 'An' else None
        # nasty hack to avoid formatting issues when groupby and color are equal (Jahr, Baujahr)
        if color == groupby:
            opnrcd_df[color + ' '] = opnrcd_df[color]
            color = color + ' '
        df = self.get_df(opnrcd_df, x_axis_name, y_axis_name, color, groupby)
        self.fig = px.scatter(
            df,
            x=x_axis_name,
            y=y_axis_name,
            color=color,
            size='Dauer (m)',
            text=labels,
            hover_name=groupby,
            )
        self.fig.update_traces(textposition='top center')
        self.fig.data[0].hovertemplate = '<b>%{hovertext}</b><br>' + x_axis_name + ' = %{x:.2f}<br>' + y_axis_name + ' = %{y:.2f}<br>' + color + ' = %{marker.color:.2f}<br> Dauer (min) = %{marker.size:.2f}<extra></extra>'
        self.fig.update_layout(transition_duration=200)

    def get_df(self, df, x_axis_name, y_axis_name, color, groupby):
        df = df.astype({'Jahr': 'int64'})
        # nasty hack to avoid formatting issues when groupby and color are equal (Jahr, Baujahr)
        if 'Jahr ' in df:
            df = df.astype({'Jahr ': 'int64'})
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
        if groupby == "Künstler" or groupby == "Strophentitel":
            return None
        else:
            return groupby