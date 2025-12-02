from powerbpy import *

import os


my_dashboard = Dashboard(os.getcwd(), "test_dashboard")

page2 = my_dashboard.new_page(page_name = "Bigfoot Map",
                              title= "Bigfoot sightings", 
                              subtitle = "By Washington Counties")

page2.add_background_image(img_path = "/home/russ/Documents/coding_projects/portfolio_projects/powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg", 
	               alpha = 51,
	               scaling_method = "Fit")

