from powerbpy import *

import os


my_dashboard = Dashboard(os.getcwd(), "test_dashboard")

# Try to add datasets
my_dashboard.add_local_csv( # data_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/colony.csv"
                              data_path = "/home/russ/Documents/coding_projects/portfolio_projects/powerbpy/examples/data/colony.csv"


)

page2 = my_dashboard.new_page(page_name = "Bigfoot Map",
                              title= "Bigfoot sightings", 
                              subtitle = "By Washington Counties")

page2.add_background_image(
                   #img_path = "C:/Users/rshea/coding_projects/powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg",
                   img_path = "/home/russ/Documents/coding_projects/portfolio_projects/powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg",
	               alpha = 51,
	               scaling_method = "Fit")

page2.add_chart(visual_id = "colonies_lost_by_year", 
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

# add a text box to the second page
page2.add_text_box(text = "Explanatory text in the bottom right corner",
                 visual_id = "page2_explain_box", 
                 height = 200,
                   width= 300,
                     x_position = 1000, 
                     y_position = 600, 
                     font_size = 15)


# add buttons

# download data button (a link to an internet address)
page2.add_button(label = "Download Data",
  visual_id = "page2_download_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 540,
  url_link = "https://www.google.com/")

# navigate back to page 1 button
page2.add_button(label = "Back to page 1",
  visual_id = "page2_back_to_page1_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 490,
  page_navigation_link = "page1")

