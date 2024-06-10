from conditions_state import ConditionsState
from vi_state import VIState

spring_variety_map: list = ["Glee", "Kelse", "Alum", "Chet", "Louise", "Ryan", "Seahawk",
                            "Whit", "Dayn", "Tekoa", "Net CL+", "Jedd"]

winter_variety_map: list = ["Rosalyn", "Otto", "Puma", "Purl", "Jasper", "Inspire", "Piranha CL+", "Jameson"]


class DataPoint:
    """
    One day data point of states and conditions of crops
    """

    def __init__(self, date: int, season: str, sensor_name: str,  # This class
                 variety_index: int, replication_variety: int,
                 vegetation_formula: str, vegetation_index_mean: float,  # VI class
                 air_temp: float, dewpoint: float, relative_humidity: float,  # Conditions class
                 soil_temp_8in: float, precipitation: float, solar_radiation: float):
        self.date: int = date
        self.season: str = season
        self.sensor_name: str = sensor_name
        self.variety_index: int = variety_index
        self.replication_variety: int = replication_variety
        self.vi_state = VIState(vegetation_formula, vegetation_index_mean)
        self.conditions_state = ConditionsState(air_temp, dewpoint, relative_humidity, soil_temp_8in,
                                                precipitation, solar_radiation)

    def get_variety_name(self) -> str:
        """
        Gets the variety name
        :return: str = Name of the wheat variety
        """
        return spring_variety_map[self.variety_index - 1]
