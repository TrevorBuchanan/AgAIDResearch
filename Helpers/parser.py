import csv

from Helpers.utility import convert_str_to_int_date, get_data_point_index, sort_data_points_by_date, \
    get_plot_missing_dates, singleton
from Helpers.interpolator import Interpolator
from Helpers.visualizer import Visualizer

from DataStructures.conditions_state import ConditionsState
from DataStructures.data_point import DataPoint
from DataStructures.plot import Plot
from DataStructures.vi_state import VIState

visualizer = Visualizer()


@singleton
class Parser:
    def __init__(self) -> None:
        self.interpolator = Interpolator()

    def parse_winter_data(self, winter_plots: list, vi_formula_target: str) -> None:
        """
        Parses the winter data provided in PullmanIOTData
        :param winter_plots: list - List of plots to parse into
        :param vi_formula_target: The type of vi to take values for
        :return: None
        """
        # Ground truth winter wheat
        file_path: str = "PullmanIOTData/GT_winter_wheat.csv"

        # (Plot) Data to get for each plot:
        # type_name, heading_date, plant_height, test_pounds_per_bushel, plot_area, experiment_name,
        # year, location, vi_formula, variety_index, replication_variety, crop_yield
        with open(file_path, mode="r") as gt_winter_file:
            csv_reader = csv.DictReader(gt_winter_file)
            for row in csv_reader:
                type_name = row['Name1']
                heading_date = int(row['Heading Date'])
                plant_height = float(row['Plant height inch'])
                test_pounds_per_bushel = float(row['Test Wt lb/bu'])
                plot_area = int(row['Plot Area'])
                experiment_name = row['Experiment Name']
                year = int(row['Year'])
                location = row['Locn']
                vi_formula = vi_formula_target
                variety_index = int(row['ENTRY'])
                if int(row['BLOC']) > 3:  # No IOT data exists for BLOC's 4-6 for winter data
                    continue
                replication_variety = int(row['BLOC'])
                crop_yield = int(row['Yield bu/a'])
                plot = Plot(type_name, heading_date, plant_height, test_pounds_per_bushel, plot_area, experiment_name,
                            year, location, vi_formula, variety_index, replication_variety, crop_yield)
                winter_plots.append(plot)

        # Full Winter Wheat Data
        file_path = "PullmanIOTData/Final_Winter_Wheat_Weather.csv"

        # Conditions and state (DataPoint) data to get for each plot:
        # date, season_type, sensor_name, variety_index, replication_variety --> DataPoint class
        # vegetation_formula, vegetation_index_mean --> VI class in DataPoint
        # air_temp, dewpoint, relative_humidity, soil_temp_8in,
        # precipitation, solar_radiation --> Conditions class in DataPoint
        with open(file_path, mode="r") as dp_winter_file:
            csv_reader = csv.DictReader(dp_winter_file)
            for row in csv_reader:
                # DataPoint specific
                date = convert_str_to_int_date(row['date'])
                season_type = row['wheat']
                sensor_name = row['sensor']
                variety_index = int(row['variety'])
                replication_variety = int(row['rep_var'])
                # VI class in DataPoint
                vi_formula = row['vi']
                if vi_formula != vi_formula_target:  # Only get values on one type of vegetation index formula
                    continue
                vi_mean = float(row['mean'])
                vi_state = VIState(vi_formula, vi_mean)
                # Conditions class in DataPoint
                air_temp = float(row['air_temp'])
                dew_point = float(row['dewpoint'])
                relative_humidity = float(row['rel_humidity'])
                soil_temp_2in = float(row['soil_temp_2_in'])
                soil_temp_8in = float(row['avg_soil_temp_8_in'])
                precipitation = float(row['precip'])
                solar_radiation = float(row['solar_rad'])
                conditions_state = ConditionsState(air_temp, dew_point, relative_humidity, soil_temp_2in,
                                                   soil_temp_8in, precipitation, solar_radiation)
                # Add the DataPoint to the Plots data
                data_point = DataPoint(date, season_type, sensor_name, variety_index,
                                       replication_variety, vi_state, conditions_state)
                winter_plots[get_data_point_index(data_point, winter_plots)].add_data_point(data_point)

        # Filter faulty plots:
        plots_to_rm = []
        for plot in winter_plots:
            if len(plot.data_points) == 0:
                plots_to_rm.append(plot)
        for p in plots_to_rm:
            winter_plots.remove(p)

        for plot in winter_plots:
            sort_data_points_by_date(plot.data_points)
            visualizer.saved_missing = get_plot_missing_dates(plot)
        self.interpolator.fill_missing_data(winter_plots)

    def parse_spring_data(self, spring_plots: list, vi_formula_target: str) -> None:
        """
        Parses the spring data provided in PullmanIOTData
        :param spring_plots: list - list of plots to parse into
        :param vi_formula_target: The type of vi to take values for
        :return: None
        """
        # Ground truth spring wheat
        file_path: str = "PullmanIOTData/GT_spring_wheat.csv"

        # (Plot) Data to get for each plot:
        # type_name, heading_date, plant_height, test_pounds_per_bushel, plot_area, experiment_name,
        # year, location, vi_formula, variety_index, replication_variety, crop_yield
        with open(file_path, mode="r") as gt_spring_file:
            csv_reader = csv.DictReader(gt_spring_file)
            for row in csv_reader:
                type_name = row['Name1']
                heading_date = int(row['Heading Date'])
                plant_height = float(row['Plant height inch'])
                test_pounds_per_bushel = float(row['Test Wt lb/bu'])
                plot_area = int(row['Plot Area'])
                if plot_area > 80:  # Skip the large areas because the no IOT data for them
                    continue
                experiment_name = row['Experiment Name']
                year = int(row['Year'])
                location = row['Locn']
                vi_formula = vi_formula_target
                variety_index = int(row['ENTRY'])
                replication_variety = int(row['BLOC'])
                crop_yield = float(row['Yield bu/a'])
                plot = Plot(type_name, heading_date, plant_height, test_pounds_per_bushel, plot_area, experiment_name,
                            year, location, vi_formula, variety_index, replication_variety, crop_yield)
                spring_plots.append(plot)

        # Full Spring Wheat Data
        file_path = "PullmanIOTData/Final_Spring_Wheat_Weather.csv"

        # Conditions and state (DataPoint) data to get for each plot:
        # date, season_type, sensor_name, variety_index, replication_variety --> DataPoint class
        # vegetation_formula, vegetation_index_mean --> VI class in DataPoint
        # air_temp, dewpoint, relative_humidity, soil_temp_8in,
        # precipitation, solar_radiation --> Conditions class in DataPoint
        with open(file_path, mode="r") as dp_spring_file:
            csv_reader = csv.DictReader(dp_spring_file)
            for row in csv_reader:
                # DataPoint specific
                date = convert_str_to_int_date(row['date'])
                season_type = row['wheat']
                sensor_name = row['sensor']
                variety_index = int(row['variety'])
                replication_variety = int(row['rep_var'])
                # VI class in DataPoint
                vi_formula = row['vi']
                if vi_formula != vi_formula_target:  # Only get values on one type of vegetation index formula
                    continue
                vi_mean = float(row['mean'])
                vi_state = VIState(vi_formula, vi_mean)
                # Conditions class in DataPoint
                air_temp = float(row['air_temp'])
                dew_point = float(row['dewpoint'])
                relative_humidity = float(row['rel_humidity'])
                soil_temp_2in = float(row['soil_temp_2_in'])
                soil_temp_8in = float(row['avg_soil_temp_8_in'])
                precipitation = float(row['precip'])
                solar_radiation = float(row['solar_rad'])
                conditions_state = ConditionsState(air_temp, dew_point, relative_humidity, soil_temp_2in,
                                                   soil_temp_8in, precipitation, solar_radiation)
                # Add the DataPoint to the Plots data
                data_point = DataPoint(date, season_type, sensor_name, variety_index,
                                       replication_variety, vi_state, conditions_state)
                spring_plots[get_data_point_index(data_point, spring_plots)].add_data_point(data_point)

        plots_to_rm = []
        for plot in spring_plots:
            if len(plot.data_points) == 0:
                plots_to_rm.append(plot)
        for p in plots_to_rm:
            spring_plots.remove(p)

        for plot in spring_plots:
            sort_data_points_by_date(plot.data_points)
            visualizer.saved_missing = get_plot_missing_dates(plot)
        self.interpolator.fill_missing_data(spring_plots)

