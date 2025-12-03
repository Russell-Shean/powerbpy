from powerbpy import *

import os


my_dashboard = Dashboard(os.getcwd(), "test_dashboard")

# Try to add datasets
my_dashboard.add_local_csv(data_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/colony.csv")

page2 = my_dashboard.new_page(page_name = "Bigfoot Map",
                              title= "Bigfoot sightings", 
                              subtitle = "By Washington Counties")

page2.add_background_image(img_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg",
	               alpha = 51,
	               scaling_method = "Fit")

page2.add_chart( 
	      page_id = "page2", 
	      chart_id = "colonies_lost_by_year", 
	      chart_type = "columnChart",
	      data_source = "colony",
	      chart_title = "Number of Bee Colonies Lost per Year",
	      x_axis_title = "Year",
	      y_axis_title = "Number of Colonies",
	      x_axis_var = "year",
	      y_axis_var = "colony_lost",
	      y_axis_var_aggregation_type = "Sum",
	      x_position = 23,
	      y_position = 158,
	      height = 524,
	      width = 603)

