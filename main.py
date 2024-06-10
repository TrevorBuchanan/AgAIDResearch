# Trevor Buchanan

# Units and labels:
# - Temperatures: Celsius
# - Yield: Bushels/Acre
# - Soil temperature depth: Inches
# - Plant height: Inches
# - Plot area: Square feet

# Notes:
# Sprint wheat crop was planted on the 25th of April
# Vegetation index (vi) formula names: cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

from plot import Plot
import csv

winter_data: list[Plot] = []
spring_data: list[Plot] = []


def is_leap_year(year: int) -> bool:
    """
    Checks if a given year is a leap year.
    :param year: int - year to check
    :return: bool - True if leap year, False otherwise
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def convert_str_to_int_date(str_date: str) -> int:
    """
    Converts string date to integer date in the Julian Date Calendar.
    Ex: 2022-06-07 to 158
    :param str_date: str - Date in form year-month-day
    :return: int - number representing the date in the Julian Date Calendar
    """
    import datetime

    # Parse the input date string
    date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    year = date.year

    # Determine if the year is a leap year
    leap = is_leap_year(year)

    # Days in each month
    days_in_month = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Calculate the Julian day
    julian_day = sum(days_in_month[:date.month - 1]) + date.day

    return julian_day


def convert_int_to_str_date(int_date: int, year: int = 2022) -> str:
    """
    Converts integer date in the Julian Date Calendar to string date.
    Ex: 158 to 2022-06-07
    :param int_date: int - Date in 1-365 or 366 if leap year
    :param year: int - Year for the conversion
    :return: str - str representing the date in the form year-month-day
    """
    # Determine if the year is a leap year
    leap = is_leap_year(year)

    # Days in each month
    days_in_month = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Find the month and day
    month = 0
    while int_date > days_in_month[month]:
        int_date -= days_in_month[month]
        month += 1

    day = int_date
    month += 1  # Adjust month since list is zero-indexed

    return f"{year:04d}-{month:02d}-{day:02d}"


def parse_winter_data(vi_formula_target: str):
    # Ground truth winter wheat
    file_path = "PullmanIOTData/GT_winter_wheat.csv"

    with open(file_path, mode="r") as gt_winter_file:
        csv_reader = csv.DictReader(gt_winter_file)

        for row in csv_reader:
            variety = row["ENTRY"]  # Replace "Date" with the actual column name
            temperature = row["BLOC"]  # Replace "Temperature" with the actual column name
            humidity = row["Humidity"]  # Replace "Humidity" with the actual column name
            print(f"Date: {date}, Temperature: {temperature}, Humidity: {humidity}")

    # Full Winter Wheat Data
    file_path = "PullmanIOTData/Final_Spring_Wheat_Weather.csv"

    with open(file_path, mode="r") as winter_file:
        csv_reader = csv.DictReader(winter_file)

        for row in csv_reader:
            date = row["date"]  # Replace "Date" with the actual column name
            temperature = row["Temperature"]  # Replace "Temperature" with the actual column name
            humidity = row["Humidity"]  # Replace "Humidity" with the actual column name
            print(f"Date: {date}, Temperature: {temperature}, Humidity: {humidity}")


def parse_sprint_data(vi_formula_target: str):
    spring_file = open("PullmanIOTData/Final_Spring_Wheat_Weather.csv", "r")


if __name__ == '__main__':
    print("AgAID Project")
