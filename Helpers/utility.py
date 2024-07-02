import datetime
import random
import numpy as np

from DataStructures.plot import Plot
from colorama import Fore, Style

# ______________________________ Utility containers _________________________________

spring_variety_map: list = ["Glee", "Kelse", "Alum", "Chet", "Louise", "Ryan", "Seahawk",
                            "Whit", "Dayn", "Tekoa", "Net CL+", "Jedd"]

winter_variety_map: list = ["Rosalyn", "Otto", "Puma", "Purl", "Jasper", "Inspire", "Piranha CL+", "Jameson"]


# _______________________________ Utility functions _________________________________

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


def get_plot_missing_dates(plot: Plot) -> list:
    """
    Gets a list of the missing dates in a plot's list of data points
    :param plot: Plot - Plot to search for missing dates in
    :return: list - List of missing dates in plot's data points
    """
    dates = []
    for data_point in plot.data_points:
        dates.append(data_point.date)
    dates.sort()
    return find_missing(dates)


def show_plot_data_missing_dates(plot: Plot) -> None:
    """
    Shows missing dates for a plot's data points
    :param plot: Plot - Plot to be checked
    :return: None
    """
    missing_dates = get_plot_missing_dates(plot)  # May need to fetch missing days from visualizer instead
    for missing_date in missing_dates:
        print("\t*", end="")
        if abs(plot.heading_date - missing_date) < 14:
            print_red('*' + convert_int_to_str_date(missing_date, 2022))
        else:
            print_green(convert_int_to_str_date(missing_date, 2022))


def find_missing(lst: list[int]) -> list[int]:
    """
    Finds the missing numbers in a sequence of in order numbers
    :param lst: list[int] - List of numbers to find missing from
    :return: List[int] - List of missing numbers in order
    """
    max_item = lst[len(lst) - 1]
    min_item = lst[0]
    missing_nums = []
    for num in range(min_item + 1, max_item):
        if num not in lst:
            missing_nums.append(num)
    return missing_nums


def print_red(string: str) -> None:
    """
    Prints text in red
    :param string: str - text to be printed
    :return: None
    """
    print(Fore.RED, string)
    print(Style.RESET_ALL, end="")


def print_green(string: str) -> None:
    """
    Prints text in green
    :param string: str - text to be printed
    :return: None
    """
    print(Fore.GREEN, string)
    print(Style.RESET_ALL, end="")


def singleton(cls):
    """
    Decorator for making a class a singleton
    :return: Instance of decorated class
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def shuffle_in_unison(a, b) -> tuple:
    """
    Shuffles two numpy arrays in unison.
    :param a: First NumPy array.
    :param b: Second NumPy array (must have the same length as a).
    :return: shuffled_a: First array shuffled in the same order as b.
    shuffled_b: Second array shuffled.
    """
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = list(range(len(a)))
    random.shuffle(permutation)

    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]

    return shuffled_a, shuffled_b


def get_plot(variety_index: int, replication_variety: int, plots: list) -> Plot:
    """
    Gets the plot with given variety and replication variety (Block)

    Parameters:
    variety_index (int): Index of variety type in variety map
    replication_variety (int): Number representing the replication variety or Block
    plots (list): List of plots to search from

    Returns
    (Plot): The plot with given values if found
    """

    def check_same_plot(plot: 'Plot') -> bool:
        return plot.variety_index == variety_index and plot.replication_variety == replication_variety

    same_plots = list(filter(check_same_plot, plots))
    if len(same_plots) > 1:
        print("More than 1 same plot")
    if len(same_plots) == 0:
        print("No same plots found")
    return same_plots[0]


def percent_error(experimental_value, theoretical_value):
    """
    Calculate the percent error between an experimental value and a theoretical value.

    Parameters:
    experimental_value (float): The value obtained from the experiment.
    theoretical_value (float): The true or accepted value.

    Returns:
    float: The percent error.
    """
    error = abs(experimental_value - theoretical_value)
    p_error = (error / abs(theoretical_value)) * 100
    return p_error
