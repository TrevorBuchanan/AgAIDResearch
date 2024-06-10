from data_point import DataPoint


class Plot:
    """
    One individual plot with a unique variety index and replication variety
    """
    def __init__(self, type_name: str, heading_date: int, plant_height: float,
                 test_pounds_per_bushel: float, plot_area: int, experiment_name: str,
                 year: int, location: str, vi_formula: str, variety_index: int, replication_variety: int):
        self.type_name: str = type_name
        self.heading_date: int = heading_date
        self.plant_height: float = plant_height
        self.test_pounds_per_bushel: float = test_pounds_per_bushel
        self.plot_area: int = plot_area
        self.experiment_name: str = experiment_name
        self.year: int = year
        self.location: str = location
        self.vi_formula: str = vi_formula
        self.variety_index: int = variety_index
        self.replication_variety: int = replication_variety
        self.data_points: list[DataPoint] = []

    def add_data_point(self, data_point) -> None:
        """
        Adds a data point to the plots list of data points
        :param data_point: An object of type DataPoint
        :return: None
        """
        self.data_points.append(data_point)

