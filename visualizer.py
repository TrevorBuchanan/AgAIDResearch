import matplotlib.pyplot as plt

from plot import Plot
from utility import get_plot_missing_dates, convert_int_to_str_date


class Visualizer:
    def __init__(self):
        self.show_yield = False

    def visualize_plot(self, plot: Plot, vi_formula: str, var_ind: int, rep_var: int) -> None:
        """
        Visualization for plot
        :return: None
        """

        dates = []
        vi_means = []
        precip_means = []
        soil_temp_2ins = []
        soil_temp_8ins = []
        air_temps = []

        min_date = plot.data_points[0].date
        print(convert_int_to_str_date(min_date))
        max_date = plot.data_points[len(plot.data_points) - 1].date

        for dp in plot.data_points:
            dates.append(dp.date)
            vi_means.append(dp.vi_state.vi_mean)
            precip_means.append(dp.conditions_state.precipitation)
            soil_temp_2ins.append(dp.conditions_state.soil_temp_2in)
            soil_temp_8ins.append(dp.conditions_state.soil_temp_8in)
            air_temps.append(dp.conditions_state.air_temp)

        plt.figure()

        plt.xlim(min_date, max_date)

        # Missing days
        for day in get_plot_missing_dates(plot):
            plt.scatter(day, 0, color='red')

        for date in dates:
            plt.scatter(date, vi_means[dates.index(date)], color='purple')
            plt.scatter(date, precip_means[dates.index(date)], color='gray')
            plt.scatter(date, soil_temp_2ins[dates.index(date)], color='brown')
            plt.scatter(date, soil_temp_8ins[dates.index(date)], color='yellow')
            plt.scatter(date, air_temps[dates.index(date)], color='orange')

        # Heading date
        plt.scatter(plot.heading_date, vi_means[dates.index(plot.heading_date)], color='blue', label='Heading date')

        # Line graphs
        plt.plot(dates, vi_means, color='purple', label=f'VI ({vi_formula}) History')
        plt.plot(dates, precip_means, color='gray', label=f'Precipitation History')
        plt.plot(dates, soil_temp_2ins, color='brown', label=f'Soil 2 in')
        plt.plot(dates, soil_temp_8ins, color='yellow', label=f'Soil 8 in')
        plt.plot(dates, air_temps, color='orange', label=f'Air temps')

        # plt.bar(max_date, plot.crop_yield, color='orange', label='Yield')
        plt.title(f'Values for Plot ({var_ind}, {rep_var})')
        plt.xlabel('Data Point Index')
        plt.ylabel('Mean')
        plt.grid(True)
        plt.legend()
        plt.show()
