from powerbpy import Dashboard

import os

dashboard_path = os.path.join(os.getcwd(), "test_dashboard")


my_dashboard = Dashboard.create(dashboard_path)


# Try to add datasets
my_dashboard.add_local_csv(
                             data_path = "examples/data/colony.csv"
)

my_dashboard.add_local_csv(
                              data_path = "examples/data/wa_bigfoot_by_county.csv"
                            )

my_dashboard.add_local_csv( 
                            data_path = "examples/data/sales_final_dataset.csv"
                            )

# add the default DateTable to the dashboard 
my_dashboard.add_tmdl(data_path = None, add_default_datetable = True)

# add pages

page1 = my_dashboard.new_page(page_name = "Bee Colonies",
	                   title= "The bees are in trouble!",
	                   subtitle = "We're losing bee colonies")


page2 = my_dashboard.new_page(page_name = "Bigfoot Map",
	                   title= "Bigfoot sightings",
	                   subtitle = "By Washington Counties")

## page 3 ------------------------------------------------------------------------------------------------------
page3 = my_dashboard.new_page(page_name = "Table Page") 

# page 4 ----------------------------------------------------------------------------------------------------------
page4 = my_dashboard.new_page(page_name = "Table Page 2") 


page1.add_background_image(
                   img_path = "examples/data/Taipei_skyline_at_sunset_20150607.jpg",
	               alpha = 51,
	               scaling_method = "Fit")

page1.add_chart(visual_id = "colonies_lost_by_year", 
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
page1.add_text_box(text = "Explanatory text in the bottom right corner",
                 visual_id = "page2_explain_box", 
                 height = 200,
                   width= 300,
                     x_position = 1000, 
                     y_position = 600, 
                     font_size = 15)


# add buttons

# download data button (a link to an internet address)
page1.add_button(label = "Download Data",
  visual_id = "page2_download_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 540,
  url_link = "https://www.google.com/")

# navigate back to page 1 button
page1.add_button(label = "Move to page 2",
  visual_id = "page1_move_to_page1_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 490,
  page_navigation_link = "page2")

## Add a map to page 3 ----------------------------------------------------------------------

page2.add_shape_map(
              visual_id = "bigfoots_by_county_map",
              data_source = "wa_bigfoot_by_county",
              shape_file_path = "examples/data/2019_53_WA_Counties9467365124727016.json",
              map_title = "Washington State Bigfoot Sightings by County",
              #map_title = "",
              location_var = "county",
              color_var = "count",
              filtering_var = "season",
              #static_bin_breaks = [0, 15.4, 30.8, 46.2, 61.6, 77.0],
              percentile_bin_breaks = [0,0.2,0.4,0.6,0.8,1],
              color_palette = ["#efb5b9",  "#e68f96","#de6a73","#a1343c", "#6b2328"],
              height = 534,
              width = 816,
              x_position = 75,
              y_position = 132,
              z_position = 2000,
              add_legend = True
              #add_legend = False
              )

# Add table to page 4 ---------------------
page3.add_table( 
              visual_id = "sales_table", 
              data_source = "sales_final_dataset", 
              variables = ["Name", "Sales First 180 Days", "Sales Last 180 Days", "Starting Size", "Ending Size"],
              x_position = 615, 
              y_position = 0, 
              height = 800, 
              width = 615,
              add_totals_row = False,
              table_title = "Store Sales Details",
              #column_widths = {"county":100,"season":50,"count":200},
              tab_order = -1001,
              z_position = 6000 )


page3.add_sanky_chart(
              visual_id = "sales_sanky", 
              data_source = "sales_final_dataset",
              chart_title="Store Starting and Ending Size",
              starting_var="Starting Size",
              starting_var_values=["Large", "Medium", "Small"], 
              ending_var="Ending Size",
              ending_var_values=["Large", "Medium", "Small"],
              values_from_var="Name", 
              x_position=0, 
              y_position=0, 
              height = 800, 
              width = 615,
)



page4.add_sanky_chart(
              visual_id = "sales_sanky", 
              data_source = "sales_final_dataset",
              chart_title="Store Starting and Ending Size",
              starting_var="Starting Size",
              starting_var_values=["Large", "Medium", "Small"], 
              ending_var="Ending Size",
              ending_var_values=["Large", "Medium", "Small"],
              link_colors=["#C29BD5","#C29BD5","#C29BD5",
                           "#F4CB93","#F4CB93","#F4CB93",
                           "#7CCDF2","#7CCDF2","#7CCDF2"],
              values_from_var="Name", 
              x_position=0, 
              y_position=0, 
              height = 800, 
              width = 615
              )


# try loading the dashboard and adding a new page....
my_dashboard2 = Dashboard.load(dashboard_path)


page5 = my_dashboard2.new_page("Page 5?")

# Try loading a page and adding a text box

page4 = my_dashboard2.load_page("page4")

page4.add_text_box(text= "A test text box", 
				 visual_id="test_box", 
				 height= 200, 
				 width=300,
				 x_position= 900, 
				 y_position= 300)

# Get a list of pages
pages = my_dashboard2.list_pages()

for page_id in pages:
  
  if page_id != "page1":
    page = my_dashboard2.load_page(page_id)
    page.add_background_image(
                   img_path = "examples/data/Taipei_skyline_at_sunset_20150607.jpg",
	               alpha = 51,
	               scaling_method = "Fit")

print(pages)