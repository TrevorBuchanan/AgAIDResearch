# Trevor Buchanan

# Units and labels:
# - Temperatures: Celsius
# - Yield: Bushels/Acre
# - Soil temperature depth: Inches
# - Plant height: Inches
# - Plot area: Square feet

# Notes:
# Sprint wheat crop was planted on the 25th of April


import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

from plot import Plot


def convert_str_to_int_date():
    pass


def convert_int_to_str_date():
    pass


def parse_winter_data():
    winter_file = open("PullmanIOTData/Final_Spring_Wheat_Weather.csv", "r")


def parse_sprint_data():
    spring_file = open("PullmanIOTData/Final_Spring_Wheat_Weather.csv", "r")


winter_data: list[Plot] = []
spring_data: list[Plot] = []

if __name__ == '__main__':
    print("AgAID Project")
