import csv

from DataStructures.conditions_state import ConditionsState
from DataStructures.data_point import DataPoint
from DataStructures.plot import Plot
from DataStructures.vi_state import VIState
from Helpers.utility import get_plot_missing_dates, insert_data_point, convert_str_to_int_date


class Interpolator:
    def __init__(self):
        pass

    def fill_missing_data(self, plots: list[Plot]) -> None:
        for plot in plots:
            missing = get_plot_missing_dates(plot)
            new_data_points = self.generate_data_points(missing, plot, plots)
            for dp in new_data_points:
                insert_data_point(dp, plot)

    def generate_data_points(self, dates: list[int], plot: Plot, plots: list[Plot]) -> list:
        new_data_points = []
        for date in dates:
            lerped_vi_mean: float = self.lerp_fill(date, dates, plot.data_points, "vi_mean")
            new_vi_state: VIState = VIState(plot.vi_formula, lerped_vi_mean)
            air_temp: float = self.other_data_point_fill(date, dates, plot.data_points, "air_temp", plots)
            dewpoint: float = self.other_data_point_fill(date, dates, plot.data_points, "dewpoint", plots)
            relative_humidity: float = self.other_data_point_fill(date, dates, plot.data_points,
                                                                  "relative_humidity", plots)
            soil_temp_2in: float = self.other_data_point_fill(date, dates, plot.data_points, "soil_temp_2in", plots)
            soil_temp_8in: float = self.other_data_point_fill(date, dates, plot.data_points, "soil_temp_8in", plots)
            precipitation: float = self.other_data_point_fill(date, dates, plot.data_points, "precipitation", plots)
            solar_radiation: float = self.other_data_point_fill(date, dates, plot.data_points, "solar_radiation", plots)
            new_conditions_state = ConditionsState(air_temp, dewpoint, relative_humidity, soil_temp_2in,
                                                   soil_temp_8in, precipitation, solar_radiation)
            new_dp = DataPoint(date, plot.data_points[0].season_type, "Interpolated", plot.variety_index,
                               plot.replication_variety, new_vi_state, new_conditions_state)
            new_data_points.append(new_dp)
        return new_data_points

    @staticmethod
    def lerp_fill(date: int, dates: list[int], data_points: list, goal_val: str) -> float:
        """
        Linearly interpolate between the closest known dates
        :param goal_val: str - The value type name to interpolate for
        :param date: int - The date that needs an interpolated value
        :param dates: list[int] - List of missing dates
        :param data_points: list[DataPoints] - Datapoints to reference values from
        :return: flaot - interpolated value for given date
        """

        def find_left_index():
            current_i = dates.index(date)
            # Iterate over the previous dates in reverse order
            for i in range(current_i, 0, -1):
                if abs(dates[i - 1] - dates[i]) > 1:
                    # Found a gap of more than 1 day
                    return dates[i] - 1
            return dates[0] - 1

        def find_right_index():
            current_i = dates.index(date)
            # Iterate over the previous dates in reverse order
            for i in range(current_i, len(dates) - 1):
                if dates[i + 1] - dates[i] > 1:
                    # Found a gap of more than 1 day
                    return dates[i] + 1

            return dates[len(dates) - 1] + 1

        def find_val(index):
            for dp in data_points:
                if goal_val == "vi_mean":
                    if dp.date == index:
                        return dp.vi_state.vi_mean
                if goal_val == "dewpoint":
                    if dp.date == index:
                        return dp.conditions_state.dewpoint
                if goal_val == "soil_temp_2in":
                    if dp.date == index:
                        return dp.conditions_state.soil_temp_2in
                if goal_val == "soil_temp_8in":
                    if dp.date == index:
                        return dp.conditions_state.soil_temp_8in
                if goal_val == "solar_radiation":
                    if dp.date == index:
                        return dp.conditions_state.soil_temp_8in
            return None

        x = date
        x1 = find_left_index()
        x2 = find_right_index()
        y1 = find_val(x1)
        y2 = find_val(x2)
        if x2 == x1:
            return y1
        slope = (y2 - y1) / (x2 - x1)
        y_int = y1 - (slope * x1)
        y_to_find = slope * x + y_int

        return y_to_find

    def other_data_point_fill(self, date: int, dates, data_points, goal_val: str, plots: list[Plot]) -> float:
        for plot in plots:
            for dp in plot.data_points:
                if dp.date == date:
                    if goal_val == "air_temp":
                        return dp.conditions_state.air_temp
                    if goal_val == "dewpoint":
                        return dp.conditions_state.dewpoint
                    if goal_val == "relative_humidity":
                        return dp.conditions_state.relative_humidity
                    if goal_val == "soil_temp_2in":
                        return dp.conditions_state.soil_temp_2in
                    if goal_val == "soil_temp_8in":
                        return dp.conditions_state.soil_temp_8in
                    if goal_val == "precipitation":
                        return dp.conditions_state.precipitation
                    if goal_val == "solar_radiation":
                        return dp.conditions_state.solar_radiation
        return self.external_weather_data_fill(plots[0].data_points[0].season_type, date, dates, data_points, goal_val)

    def external_weather_data_fill(self, season: str, date: int, dates, data_points, goal_val: str) -> float:
        if season == "winter":
            file_path: str = "GapFillWeatherData/22PULSATW.csv"
        else:
            file_path: str = "GapFillWeatherData/22PULSATS.csv"

        with open(file_path, mode="r") as weather_file:
            csv_reader = csv.DictReader(weather_file)
            for row in csv_reader:
                fill_date: int = convert_str_to_int_date(row['date'])
                if fill_date == date:
                    if goal_val == "solar_radiation":
                        continue
                    if goal_val in row:
                        return float(row[goal_val])

        return self.lerp_fill(date, dates, data_points, goal_val)
