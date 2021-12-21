from abstract_view import AstractView

class ViewScatter(AstractView):

    def generate_fig(self, opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure):
        # return super().generate_fig(opnrcd_df, normalized_time_series, x_axis_name, y_axis_name, years, measure)