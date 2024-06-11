# By: Trevor Buchanan


# Units and labels:
# - Temperatures: Celsius
# - Yield: Bushels/Acre
# - Soil temperature depth: Inches
# - Plant height: Inches
# - Plot area: Square feet


# Notes:
# Sprint wheat crop was planted on the 25th of April
# Vegetation index (vi) formula names: cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
# Labels in full data and ground truth data: variety <-> ENTRY | replication_variable <-> BLOC


# Libraries
import matplotlib.pyplot as plt
import numpy as np

from plot import Plot
import csv

from utility import index_of_variety

winter_data: list[Plot] = []
spring_data: list[Plot] = []


def parse_winter_data(vi_formula_target: str):
    # Ground truth winter wheat
    file_path: str = "PullmanIOTData/GT_winter_wheat.csv"

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
            replication_variety = int(row['BLOC'])
            crop_yield = int(row['Yield bu/a'])
            plot = Plot(type_name, heading_date, plant_height, test_pounds_per_bushel, plot_area, experiment_name,
                        year, location, vi_formula, variety_index, replication_variety, crop_yield)
            winter_data.append(plot)
            print(plot)


    # Full Winter Wheat Data
    file_path = "PullmanIOTData/Final_Spring_Wheat_Weather.csv"

    with open(file_path, mode="r") as winter_file:
        csv_reader = csv.DictReader(winter_file)
        for row in csv_reader:
            pass


def parse_sprint_data(vi_formula_target: str):
    spring_file = open("PullmanIOTData/Final_Spring_Wheat_Weather.csv", "r")


if __name__ == '__main__':
    print("AgAID Project")
    parse_winter_data("ndvi")
