import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from scipy.stats import pearsonr, spearmanr
from DataStructures.plot import Plot
from Helpers.utility import convert_int_to_str_date, spring_variety_map, winter_variety_map, \
    singleton, get_plot


@singleton
class Visualizer:
    def __init__(self):
        # Visual settings
        self.line_mode = False
        self.point_mode = False
        # Data selection
        self.show_vi_mean = False
        self.show_air_temp = False
        self.show_dew_point = False
        self.show_relative_humidity = False
        self.show_soil_temp_2in = False
        self.show_soil_temp_8in = False
        self.show_precipitation = False
        self.show_solar_radiation = False
        # Result data selection
        self.show_heading_date = False
        self.show_plant_height = False
        self.show_test_pounds_per_bushel = False
        self.show_yield = False
        self.show_prediction = False

    def visualize_plots(self, plots: list[Plot], entry_bloc_pairs: list[tuple],
                        predictions=None) -> None:
        """
        Create a graph visualization of given plots' data
        :param plots: list[Plot] - List of all plots
        :param entry_bloc_pairs: list[tuple] - List of entry block pairs to create visualization for
        :param predictions: list[float] - Optional list of predictions from ML model
        :return: None
        """

        # Start graph figure
        # plt.style.use('dark_background')
        if predictions is None:
            predictions = []
        plt.figure(figsize=(16, 8))
        predictions_patch = mpatches.Patch(color='papayawhip', label='Yield predictions')
        vi_patch = mpatches.Patch(color='purple', label='VI Mean')
        air_temp_patch = mpatches.Patch(color='orange', label='Air Temp')
        dew_point_patch = mpatches.Patch(color='cyan', label='Dew point')
        relative_hum_patch = mpatches.Patch(color='teal', label='Relative humidity')
        soil_temp_2in_patch = mpatches.Patch(color='brown', label='Soil Temp 2in')
        soil_temp_8in_patch = mpatches.Patch(color='yellow', label='Soil Temp 8in')
        precip_patch = mpatches.Patch(color='gray', label='Precipitation')
        solar_rad_patch = mpatches.Patch(color='pink', label='Solar radiation')
        heading_date_patch = mpatches.Patch(color='blue', label='Heading date')
        plant_height_patch = mpatches.Patch(color='green', label='Plant height')
        test_pounds_per_bushel_patch = mpatches.Patch(color='coral', label='Lbs/bushel')
        yield_patch = mpatches.Patch(color='olive', label='Yield')
        handles = []
        if self.show_prediction:
            handles.append(predictions_patch)
        if self.show_vi_mean:
            handles.append(vi_patch)
        if self.show_air_temp:
            handles.append(air_temp_patch)
        if self.show_dew_point:
            handles.append(dew_point_patch)
        if self.show_relative_humidity:
            handles.append(relative_hum_patch)
        if self.show_soil_temp_2in:
            handles.append(soil_temp_2in_patch)
        if self.show_soil_temp_8in:
            handles.append(soil_temp_8in_patch)
        if self.show_precipitation:
            handles.append(precip_patch)
        if self.show_solar_radiation:
            handles.append(solar_rad_patch)
        if self.show_heading_date:
            handles.append(heading_date_patch)
        if self.show_plant_height:
            handles.append(plant_height_patch)
        if self.show_test_pounds_per_bushel:
            handles.append(test_pounds_per_bushel_patch)
        if self.show_yield:
            handles.append(yield_patch)

        # Initialize vars
        min_date = 0
        max_date = 0
        offset = 0
        season = ""
        for pair in entry_bloc_pairs:
            # Get correct plot
            plot = get_plot(pair[0], pair[1], plots)
            if plot.data_points[0].season_type == "winter":
                var = winter_variety_map[plot.variety_index - 1]
            else:
                var = spring_variety_map[plot.variety_index - 1]
                season = "spring"
            print(f'Variety: {var}')

            # Lists to hold each data values
            dates = []
            vi_means = []
            air_temps = []
            dew_points = []
            relative_hums = []
            soil_temp_2ins = []
            soil_temp_8ins = []
            precip_means = []
            solar_rads = []

            # Get min and max range dates of graph
            min_date = plot.data_points[0].date
            max_date = plot.data_points[len(plot.data_points) - 1].date

            # Get plot data
            for dp in plot.data_points:
                dates.append(dp.date)
                if self.show_vi_mean:
                    vi_means.append(dp.vi_state.vi_mean * 200)  # TODO: Change temp val back
                if self.show_air_temp:
                    air_temps.append(dp.conditions_state.air_temp)
                if self.show_dew_point:
                    dew_points.append(dp.conditions_state.dewpoint)
                if self.show_relative_humidity:
                    relative_hums.append(dp.conditions_state.relative_humidity)
                if self.show_soil_temp_2in:
                    soil_temp_2ins.append(dp.conditions_state.soil_temp_2in)
                if self.show_soil_temp_8in:
                    soil_temp_8ins.append(dp.conditions_state.soil_temp_8in)
                if self.show_precipitation:
                    precip_means.append(dp.conditions_state.precipitation)
                if self.show_solar_radiation:
                    solar_rads.append(dp.conditions_state.solar_radiation)

            # Point graphs
            if self.point_mode:
                for date in dates:
                    index = dates.index(date)
                    # VI mean
                    if self.show_vi_mean:
                        plt.scatter(date, vi_means[index], color='purple')
                    # Air temp
                    if self.show_air_temp:
                        plt.scatter(date, air_temps[index], color='orange')
                    # Dew point
                    if self.show_dew_point:
                        plt.scatter(date, dew_points[index], color='cyan')
                    # Relative humidity
                    if self.show_relative_humidity:
                        plt.scatter(date, relative_hums[index], color='teal')
                    # Soil temp 2 in
                    if self.show_soil_temp_2in:
                        plt.scatter(date, soil_temp_2ins[index], color='brown')
                    # Soil temp 8 in
                    if self.show_soil_temp_8in:
                        plt.scatter(date, soil_temp_8ins[index], color='yellow')
                    # Precipitation
                    if self.show_precipitation:
                        plt.scatter(date, precip_means[index], color='gray')
                    # Solar radiation
                    if self.show_solar_radiation:
                        plt.scatter(date, solar_rads[index], color='pink')

            if self.show_prediction and predictions:
                last_working_i = 0
                for date in dates:
                    index = dates.index(date)
                    # Yield prediction
                    if len(predictions) > 0:
                        if index >= len(predictions):
                            plt.bar(date, predictions[last_working_i], color='papayawhip')
                        else:
                            plt.bar(date, predictions[index], color='papayawhip')
                            last_working_i = index

            # Line graphs
            if self.line_mode:
                if self.show_vi_mean:
                    plt.plot(dates, vi_means, color='purple')
                if self.show_air_temp:
                    plt.plot(dates, air_temps, color='orange')
                if self.show_dew_point:
                    plt.plot(dates, dew_points, color='cyan')
                if self.show_relative_humidity:
                    plt.plot(dates, relative_hums, color='teal')
                if self.show_soil_temp_2in:
                    plt.plot(dates, soil_temp_2ins, color='brown')
                if self.show_soil_temp_8in:
                    plt.plot(dates, soil_temp_8ins, color='yellow')
                if self.show_precipitation:
                    plt.plot(dates, precip_means, color='gray')
                if self.show_solar_radiation:
                    plt.plot(dates, solar_rads, color='pink')

            # Heading date
            if self.show_heading_date:
                if len(vi_means) > 0:
                    plt.scatter(plot.heading_date, vi_means[dates.index(plot.heading_date)], color='blue')
                else:
                    plt.scatter(plot.heading_date, 0, color='blue')
                print("Heading date: ", end="")
                print(convert_int_to_str_date(plot.heading_date))

            # Plant height
            if self.show_plant_height:
                plt.bar(max_date + 20 + offset, plot.plant_height, color='green')

            # Test pounds per bushel
            if self.show_test_pounds_per_bushel:
                plt.bar(max_date + 10 + offset, plot.test_pounds_per_bushel, color='coral')

            # Yield
            if self.show_yield:
                plt.bar(max_date + offset, plot.crop_yield, color='olive')
                print(f'Actual yield: {plot.crop_yield}')
            if self.show_prediction and predictions:
                print(f'Final expected yield: {predictions[len(predictions) - 1]}')
            offset += 1

        # Graph logic
        if self.show_plant_height:
            plt.xlim(min_date, max_date + 21 + offset)
        elif self.show_test_pounds_per_bushel:
            plt.xlim(min_date, max_date + 11 + offset)
        else:
            plt.xlim(min_date, max_date + 1 + offset)
        # Make title string
        title_str: str = "Values for Plots: "
        for pair in entry_bloc_pairs:
            if season == 'spring':
                variety = spring_variety_map[pair[0] - 1]
            else:
                variety = spring_variety_map[pair[1] - 1]
            title_str += str(pair) + " " + variety + " "

        plt.title(title_str)
        plt.xlabel('Dates')
        plt.ylabel('Plot Values')
        plt.grid(True)
        plt.legend(handles=handles)
        plt.tight_layout()
        plt.show()

    def visualize_variety(self, plots: list[Plot], target_variety: str) -> None:
        """
        Visualize all plots of a given variety
        :param plots: list[Plot] - List of all plots
        :param target_variety: str - Variety name to show visualization for
        :return: None
        """
        season = plots[0].data_points[0].season_type
        entry_bloc_pairs = []
        for plot in plots:
            if season == 'spring':
                variety_str = spring_variety_map[plot.variety_index - 1]
            else:
                variety_str = winter_variety_map[plot.variety_index - 1]
            if variety_str == target_variety:
                entry_bloc_pairs.append((plot.variety_index, plot.replication_variety))

        self.visualize_by_plots(plots, entry_bloc_pairs)

    def visualize_num_plots(self, plots: list[Plot], num: int) -> None:
        entry_bloc_pairs = []
        total = 0
        for plot in plots:
            if total >= num:
                break
            total += 1
            entry_bloc_pairs.append((plot.variety_index, plot.replication_variety))

        self.visualize_by_plots(plots, entry_bloc_pairs)

    def visualize_by_plots(self, plots: list[Plot], entry_bloc_pairs: list[tuple], predictions=None) -> None:
        """
        Create a graph visualization of given plots' data coloring by each plot
        :param plots: list[Plot] - List of all plots
        :param entry_bloc_pairs: list[tuple] - List of entry block pairs to create visualization for
        :param predictions: list[float] - Optional list of predictions from ML model
        :return: None
        """

        # Start graph figure
        if predictions is None:
            predictions = []
        plt.figure(figsize=(16, 8))

        # Initialize colormap
        num_pairs = len(entry_bloc_pairs)
        colormap = plt.get_cmap('hsv', num_pairs + 1)

        # Initialize vars
        min_date = 0
        max_date = 0
        offset = 0
        for idx, pair in enumerate(entry_bloc_pairs):
            # Get correct plot
            plot = get_plot(pair[0], pair[1], plots)

            # Lists to hold each data values
            dates = []
            vi_means = []
            air_temps = []
            dew_points = []
            relative_hums = []
            soil_temp_2ins = []
            soil_temp_8ins = []
            precip_means = []
            solar_rads = []

            # Get min and max range dates of graph
            min_date = plot.data_points[0].date
            max_date = plot.data_points[len(plot.data_points) - 1].date

            # Get plot data
            for dp in plot.data_points:
                dates.append(dp.date)
                if self.show_vi_mean:
                    vi_means.append(dp.vi_state.vi_mean)
                if self.show_air_temp:
                    air_temps.append(dp.conditions_state.air_temp)
                if self.show_dew_point:
                    dew_points.append(dp.conditions_state.dewpoint)
                if self.show_relative_humidity:
                    relative_hums.append(dp.conditions_state.relative_humidity)
                if self.show_soil_temp_2in:
                    soil_temp_2ins.append(dp.conditions_state.soil_temp_2in)
                if self.show_soil_temp_8in:
                    soil_temp_8ins.append(dp.conditions_state.soil_temp_8in)
                if self.show_precipitation:
                    precip_means.append(dp.conditions_state.precipitation)
                if self.show_solar_radiation:
                    solar_rads.append(dp.conditions_state.solar_radiation)

            # Generate color for the current plot
            plot_color = colormap(idx / num_pairs)

            # Point graphs
            if self.point_mode:
                for date in dates:
                    index = dates.index(date)
                    # VI mean
                    if self.show_vi_mean:
                        plt.scatter(date, vi_means[index], color=plot_color)
                    # Air temp
                    if self.show_air_temp:
                        plt.scatter(date, air_temps[index], color=plot_color)
                    # Dew point
                    if self.show_dew_point:
                        plt.scatter(date, dew_points[index], color=plot_color)
                    # Relative humidity
                    if self.show_relative_humidity:
                        plt.scatter(date, relative_hums[index], color=plot_color)
                    # Soil temp 2 in
                    if self.show_soil_temp_2in:
                        plt.scatter(date, soil_temp_2ins[index], color=plot_color)
                    # Soil temp 8 in
                    if self.show_soil_temp_8in:
                        plt.scatter(date, soil_temp_8ins[index], color=plot_color)
                    # Precipitation
                    if self.show_precipitation:
                        plt.scatter(date, precip_means[index], color=plot_color)
                    # Solar radiation
                    if self.show_solar_radiation:
                        plt.scatter(date, solar_rads[index], color=plot_color)

            if self.show_prediction and predictions:
                last_working_i = 0
                for date in dates:
                    index = dates.index(date)
                    # Yield prediction
                    if len(predictions) > 0:
                        if index >= len(predictions):
                            plt.bar(date, predictions[last_working_i], color='papayawhip')
                        else:
                            plt.bar(date, predictions[index], color='papayawhip')
                            last_working_i = index

            # Line graphs
            if self.line_mode:
                if self.show_vi_mean:
                    plt.plot(dates, vi_means, color=plot_color)
                if self.show_air_temp:
                    plt.plot(dates, air_temps, color=plot_color)
                if self.show_dew_point:
                    plt.plot(dates, dew_points, color=plot_color)
                if self.show_relative_humidity:
                    plt.plot(dates, relative_hums, color=plot_color)
                if self.show_soil_temp_2in:
                    plt.plot(dates, soil_temp_2ins, color=plot_color)
                if self.show_soil_temp_8in:
                    plt.plot(dates, soil_temp_8ins, color=plot_color)
                if self.show_precipitation:
                    plt.plot(dates, precip_means, color=plot_color)
                if self.show_solar_radiation:
                    plt.plot(dates, solar_rads, color=plot_color)

            # Heading date
            if self.show_heading_date:
                if len(vi_means) > 0:
                    plt.scatter(plot.heading_date, vi_means[dates.index(plot.heading_date)], color=plot_color)
                else:
                    plt.scatter(plot.heading_date, 0, color=plot_color)
                print("Heading date: ", end="")
                print(convert_int_to_str_date(plot.heading_date))

            # Plant height
            if self.show_plant_height:
                plt.bar(max_date + 20 + offset, plot.plant_height, color=plot_color)

            # Test pounds per bushel
            if self.show_test_pounds_per_bushel:
                plt.bar(max_date + 10 + offset, plot.test_pounds_per_bushel, color=plot_color)

            # Yield
            if self.show_yield:
                plt.bar(max_date + offset, plot.crop_yield / 200, color=plot_color)
                print(f'Actual yield: {plot.crop_yield}')
            if self.show_prediction and predictions:
                print(f'Final expected yield: {predictions[len(predictions) - 1]}')
            offset += 1

        # Graph logic
        if self.show_plant_height:
            plt.xlim(min_date, max_date + 21 + offset)
        elif self.show_test_pounds_per_bushel:
            plt.xlim(min_date, max_date + 11 + offset)
        else:
            plt.xlim(min_date, max_date + 1 + offset)
        # Make title string
        title_str: str = "Values for Plots: "
        for pair in entry_bloc_pairs:
            title_str += str(pair) + " "
        plt.title(title_str)
        plt.xlabel('Dates')
        plt.ylabel('Plot Values')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_avg_vi_correspondence(plots: list[Plot]) -> None:
        """
        Create a graph of the correspondence between the average vi and the yield
        :param plots: list[Plot] - list of plots to create correspondence from
        :return: None
        """
        def get_avg_vi(data_points: list, start_i, end_i):
            total = 0
            count = 0
            for i in range(start_i, end_i):
                if count >= end_i - start_i:
                    break
                count += 1
                total += data_points[i].vi_state.vi_mean
            return total / count

        season = plots[0].data_points[0].season_type
        # Define a color map based on variety_index
        color_map = {
            0: 'red',
            1: 'green',
            2: 'blue',
            3: 'purple',
            4: 'orange',
            5: 'yellow',
            6: 'gray',
            7: 'salmon',
            8: 'pink',
            9: 'wheat',
            10: 'teal',
            11: 'cyan'
        }

        # Best vals
        best_corr = 0
        best_split_size = 0
        best_offset = 0

        # Loop to search all correlations
        split_size = 50
        while split_size > 49:
            split_offset = 0
            while split_size + split_offset <= 50:
                vi_avgs = []
                yields = []
                for p in plots:
                    vi_avgs.append(get_avg_vi(p.data_points, split_offset, split_offset + split_size))
                    yields.append(p.crop_yield)
                # Pearson Correlation
                pearson_corr, _ = pearsonr(vi_avgs, yields)
                if abs(pearson_corr) > abs(best_corr):
                    best_corr = pearson_corr
                    best_split_size = split_size
                    best_offset = split_offset
                split_offset += 1
            split_size -= 1

        print(f'Best split size: {best_split_size}')
        print(f'Best offset: {best_offset}')
        print(f'Best correlation: {best_corr}')

        vi_avgs = []
        yields = []
        colors = []
        for p in plots:
            colors.append(color_map.get(p.variety_index - 1, 'black'))
            vi_avgs.append(get_avg_vi(p.data_points, best_offset, best_offset + best_split_size))
            yields.append(p.crop_yield)

        # Create the plot
        plt.figure(figsize=(16, 8))
        plt.scatter(vi_avgs, yields, c=colors, marker='o')

        # Create custom legend handles
        if season == "winter":
            trimmed_color_map = {k: v for k, v in list(color_map.items())[:8]}
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                       markersize=10, label=f'{winter_variety_map[i]}')
                for i, color in trimmed_color_map.items()
            ]
        else:
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                       markersize=10, label=f'{spring_variety_map[i]}')
                for i, color in color_map.items()
            ]
        plt.legend(handles=legend_elements, title="Variety Index")

        # Customize the plot
        plt.xlabel('VI Averages')
        plt.ylabel('Yields')
        plt.title('VI to Yield')
        plt.tight_layout()
        plt.grid(True)

        # Display the plot
        plt.show()

    @staticmethod
    def visualize_heading_date_correlation(plots: list[Plot]) -> None:
        """
        Create a graph of the correspondence between the VI at the heading date and the yield
        :param plots: list[Plot] - list of plots to create correspondence from
        :return: None
        """
        def get_vi_at_heading_date(data_points: list, heading_date: int):
            for dp in data_points:
                if dp.date == heading_date:
                    return dp.vi_state.vi_mean
            return None
        season = plots[0].data_points[0].season_type
        # Define a color map based on variety_index
        color_map = {
            0: 'red',
            1: 'green',
            2: 'blue',
            3: 'purple',
            4: 'orange',
            5: 'yellow',
            6: 'gray',
            7: 'salmon',
            8: 'pink',
            9: 'wheat',
            10: 'teal',
            11: 'cyan'
        }

        vi_vals = []
        yields = []
        colors = []
        for p in plots:
            colors.append(color_map.get(p.variety_index - 1, 'black'))
            vi_vals.append(get_vi_at_heading_date(p.data_points, p.heading_date))
            yields.append(p.crop_yield)

        # Pearson Correlation
        pearson_corr, _ = pearsonr(vi_vals, yields)
        print(f'VI at heading date correlation: {pearson_corr}')

        # Create the plot
        plt.figure(figsize=(16, 8))
        plt.scatter(vi_vals, yields, c=colors, marker='o')

        # Create custom legend handles
        if season == "winter":
            trimmed_color_map = {k: v for k, v in list(color_map.items())[:8]}
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                       markersize=10, label=f'{winter_variety_map[i]}')
                for i, color in trimmed_color_map.items()
            ]
        else:
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                       markersize=10, label=f'{spring_variety_map[i]}')
                for i, color in color_map.items()
            ]
        plt.legend(handles=legend_elements, title="Variety Index")

        # Customize the plot
        plt.xlabel('VI at Heading date')
        plt.ylabel('Yields')
        plt.title('VI to Yield')
        plt.tight_layout()
        plt.grid(True)

        # Display the plot
        plt.show()
