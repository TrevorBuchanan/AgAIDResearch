from DataStructures.plot import Plot
from Helpers.utility import get_plot_missing_dates


class Interpolator:
    def fill_missing_data(self, plots: list[Plot]):
        for plot in plots:
            missing = get_plot_missing_dates(plot)
            print(missing)

    def lerp_fill(self):
        pass

    def other_data_point_fill(self):
        pass

    def external_weather_data_fill(self):
        pass
