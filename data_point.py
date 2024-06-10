spring_variety_map: list = ["Glee", "Kelse", "Alum", "Chet", "Louise", "Ryan", "Seahawk",
                            "Whit", "Dayn", "Tekoa", "Net CL+", "Jedd"]

winter_variety_map: list = ["Rosalyn", "Otto", "Puma", "Purl", "Jasper", "Inspire", "Piranha CL+", "Jameson"]


class DataPoint:
    def __init__(self, date: int, season: str, sensor_name: str, variety_index: int,
                 replication_variety: int, vegetation_formula: str, vegetation_index_mean: float):
        self.date: int = date
        self.season: str = season
        self.sensor_name: str = sensor_name
        self.variety_index: int = variety_index
        self.replication_variety: int = replication_variety
        self.vegetation_formula: str = vegetation_formula
        self.vegetation_index_mean: float = vegetation_index_mean

    def get_variety_name(self) -> str:
        """
        Gets the variety name
        :return: str = Name of the wheat variety
        """
        return spring_variety_map[self.variety_index - 1]
