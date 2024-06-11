import datetime

from plot import Plot
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

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


def index_of_variety(variety_name: str) -> int:
    """
    Gets the index of a given variety type
    :param variety_name: str - the name of the type of crop
    :return: int - the index of the type
    """
    if variety_name in winter_variety_map:
        return winter_variety_map.index(variety_name) + 1
    if variety_name in spring_variety_map:
        return spring_variety_map.index(variety_name) + 1
    return 0


def get_data_point_index(data_point, plots: list[Plot]) -> int:
    """
    Gets the index of the plot that should hold the specific given data point
    :param plots: List[Plots] - List to find the index in
    :param data_point: DataPoint
    :return: int - index for data_point, -1 if none found, or -2 if multiple found
    """
    count = 0
    index = 0

    for i, plot in enumerate(plots):
        if plot.replication_variety == data_point.replication_variety and \
                plot.variety_index == data_point.variety_index:
            count += 1
            index = i

    if count == 0:
        return -1
    elif count > 1:
        return -2
    else:
        return index


def show_plot_data_missing_dates(plot: Plot) -> None:
    """
    Shows missing dates for a plot's data points
    :param plot: Plot - Plot to be checked
    :return: None
    """
    dates = []
    for data_point in plot.data_points:
        dates.append(data_point.date)
    dates.sort()
    missing_dates = find_missing(dates)
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


def get_plot(variety_index: int, replication_variety: int, plots: list) -> Plot:
    def check_same_plot(plot: 'Plot') -> bool:
        return plot.variety_index == variety_index and plot.replication_variety == replication_variety

    same_plots = list(filter(check_same_plot, plots))
    if len(same_plots) > 1:
        print("More than 1 same plot")
    return same_plots[0]


def visualize_plot(plot: Plot, vi_formula: str, var_ind: int, rep_var: int) -> None:
    """
    Visualization for plot
    :return: None
    """
    winter_vi_for_plot = []
    winter_precipitation_for_plot = []

    for dp in plot.data_points:
        winter_vi_for_plot.append(dp.vi_state.vi_mean)
        winter_precipitation_for_plot.append(dp.conditions_state.precipitation)

    plt.figure()
    plt.plot(winter_vi_for_plot, label=f'VI ({vi_formula}) History')
    plt.plot(winter_precipitation_for_plot, label=f'Precipitation History')
    plt.bar(len(plot.data_points) - 1, plot.crop_yield, color='orange', label='Yield')
    plt.title(f'Values for Plot ({var_ind}, {rep_var})')
    plt.xlabel('Data Point Index')
    plt.ylabel('Mean')
    plt.grid(True)
    plt.legend()
    plt.show()
