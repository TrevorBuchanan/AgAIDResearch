from utility import sort_data_points_by_date


class Plot:
    """
    One individual plot with a unique variety index and replication variety
    """
    def __init__(self, type_name: str, heading_date: int, plant_height: float,
                 test_pounds_per_bushel: float, plot_area: int, experiment_name: str, year: int,
                 location: str, vi_formula: str, variety_index: int, replication_variety: int, crop_yield: float):
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
        self.crop_yield: float = crop_yield
        self.data_points: list = []

    def __repr__(self):
        return (f"Plot(type_name={self.type_name}, heading_date={self.heading_date}, plant_height={self.plant_height}, "
                f"test_pounds_per_bushel={self.test_pounds_per_bushel}, plot_area={self.plot_area}, "
                f"experiment_name={self.experiment_name}, year={self.year}, location={self.location}, "
                f"vi_formula={self.vi_formula}, variety_index={self.variety_index}, "
                f"replication_variety={self.replication_variety}, crop_yield={self.crop_yield}, "
                f"data_points={self.data_points})")

    def add_data_point(self, data_point) -> None:
        """
        Adds a data point to the plots list of data points
        :param data_point: An object of type DataPoint
        :return: None
        """
        self.data_points.append(data_point)

    def sort_points(self) -> None:
        """
        Sorts the data points in plot
        :return: None
        """
        sort_data_points_by_date(self.data_points)
