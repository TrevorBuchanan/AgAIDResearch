# By: Trevor Buchanan

from DataStructures.plot import Plot

from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

# cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
winter_plots: list[Plot] = []
spring_plots: list[Plot] = []

# Create visualizer
visualizer = Visualizer()

if __name__ == '__main__':
    print("AgAID Project\n")

    # Parsing selections
    season = "spring"
    vi_formula = "ndvi"
    target_variety = "Seahawk"

    # Perform parsing based on selections
    parser = Parser()
    if season == "spring":
        parser.parse_spring_data(spring_plots, vi_formula)
    elif season == "winter":
        parser.parse_winter_data(winter_plots, vi_formula)

    # Visual settings
    visualizer.line_mode = True
    visualizer.point_mode = True
    # Data selection
    visualizer.show_missing_dates = True
    visualizer.show_vi_mean = True
    # visualizer.show_air_temp = True
    # visualizer.show_dew_point = True
    # visualizer.show_relative_humidity = True
    # visualizer.show_soil_temp_2in = True
    # visualizer.show_soil_temp_8in = True
    # visualizer.show_precipitation = True
    # visualizer.show_solar_radiation = True
    # Result data selection
    visualizer.show_heading_date = True
    # visualizer.show_plant_height = True
    # visualizer.show_test_pounds_per_bushel = True
    # visualizer.show_yield = True

    # Individual plot visualization
    # Entry, Block (1-3)
    # entry_bloc_pairs = [(7, 1)]
    # if season == "spring":
    #     visualizer.visualize_plots(spring_plots, entry_bloc_pairs)
    # elif season == "winter":
    #     visualizer.visualize_plots(winter_plots, entry_bloc_pairs)

    # Variety plot visualization
    if season == "spring":
        visualizer.visualize_variety(spring_plots, target_variety)
    elif season == "winter":
        visualizer.visualize_variety(winter_plots, target_variety)
