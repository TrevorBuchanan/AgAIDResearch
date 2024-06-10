class ConditionsState:
    def __init__(self, air_temp: float, dewpoint: float, relative_humidity: float,
                 soil_temp_8in: float, precipitation: float, solar_radiation: float):
        self.air_temp: float = air_temp
        self.dewpoint: float = dewpoint
        self.relative_humidity: float = relative_humidity
        self.soil_temp_8in: float = soil_temp_8in
        self.precipitation: float = precipitation
        self.solar_radiation: float = solar_radiation
