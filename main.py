# By: Trevor Buchanan


# Units and labels:
# - Temperatures: Celsius
# - Yield: Bushels/Acre
# - Soil temperature depth: Inches
# - Plant height: Inches
# - Plot area: Square feet


# Notes:
# - Sprint wheat crop was planted on the 25th of April
# - Vegetation index (vi) formula names: cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
# - The vi used will only be the 'mean' value for each data point
# - Labels in full data and ground truth data: variety_index <-> variety <-> ENTRY | replication_variable <-> BLOC
# - The soil temperature measurement used is the 8-inch average
# - Missing data points for plot Block: 3, Entry: 2 | Block: 3, Entry: 4 | Block: 3, Entry: 8 | Block: 3, Entry: 6


# Libraries
import matplotlib.pyplot as plt
import numpy as np

from conditions_state import ConditionsState
from data_point import DataPoint
from plot import Plot
import csv

from utility import convert_str_to_int_date, get_data_point_index
from vi_state import VIState

winter_plots: list[Plot] = []
spring_plots: list[Plot] = []


def parse_winter_data(vi_formula_target: str):
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
            if int(row['BLOC']) > 3:  # No IOT data exists for BLOC's 4-6
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
    with open(file_path, mode="r") as winter_file:
        csv_reader = csv.DictReader(winter_file)
        for row in csv_reader:
            # DataPoint specific
            date = convert_str_to_int_date(row['date'])
            season_type = row['wheat']
            sensor_name = row['sensor']
            variety_index = int(row['variety'])
            replication_variety = int(row['rep_var'])
            # VI class in DataPoint
            vegetation_formula = row['vi']
            vegetation_index_mean = float(row['mean'])
            vi_state = VIState(vegetation_formula, vegetation_index_mean)
            # Conditions class in DataPoint
            air_temp = float(row['air_temp'])
            dew_point = float(row['dewpoint'])
            relative_humidity = float(row['rel_humidity'])
            soil_temp_8in = float(row['avg_soil_temp_8_in'])
            precipitation = float(row['precip'])
            solar_radiation = float(row['solar_rad'])
            conditions_state = ConditionsState(air_temp, dew_point, relative_humidity,
                                               soil_temp_8in, precipitation, solar_radiation)
            # Add the DataPoint to the Plots data
            data_point = DataPoint(date, season_type, sensor_name, variety_index,
                                   replication_variety, vi_state, conditions_state)
            winter_plots[get_data_point_index(data_point, winter_plots)].add_data_point(data_point)

    # Filter faulty plots:
    for plot in winter_plots:
        if len(plot.data_points) == 0:
            print(f'Missing data points for plot Block: {plot.replication_variety}, Entry: {plot.variety_index}')
        else:
            print(f'Data points length: {len(plot.data_points)}')


def parse_sprint_data(vi_formula_target: str):
    spring_file = open("PullmanIOTData/Final_Spring_Wheat_Weather.csv", "r")


if __name__ == '__main__':
    print("AgAID Project")
    parse_winter_data("ndvi")
