class Plot:
    def __init__(self, type_name: str, heading_date: int, plant_height: float, test_pounds_per_bushel: float,
                 plot_area: int, experiment_name: str, year: int, location: str):
        self.type_name: str = type_name
        self.heading_date: int = heading_date
        self.plant_height: float = plant_height
        self.test_pounds_per_bushel: float = test_pounds_per_bushel
        self.plot_area: int = plot_area
        self.experiment_name: str = experiment_name
        self.year: int = year
        self.location: str = location
