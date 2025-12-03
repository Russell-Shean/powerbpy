from powerbpy import *

import os


my_dashboard = Dashboard(os.getcwd(), "test_dashboard")

# Try to add datasets
#my_dashboard.add_local_csv(data_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/colony.csv")

page2 = my_dashboard.new_page(page_name = "Bigfoot Map",
                              title= "Bigfoot sightings", 
                              subtitle = "By Washington Counties")

page2.add_background_image(img_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg",
	               alpha = 51,
	               scaling_method = "Fit")

