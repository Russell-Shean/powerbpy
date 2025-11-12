import powerbpy as PBI

import os

# Define file paths -----------------------------------------------------------------------------------------

# report_name = "test_dashboard"
report_name = "test_dashboard"
report_location = os.getcwd()

dashboard_path = os.path.join(report_location, report_name)



# Create a new dashboard -----------------------------------------------------------------------------------------
PBI.create_new_dashboard(report_location, report_name)

# add data -------------------------------------------------------------------------------------------------------
# add locally stored csv files to the new dashboard
PBI.add_local_csv(dashboard_path, "colony.csv")
PBI.add_local_csv(dashboard_path, "wa_bigfoot_by_county.csv")
PBI.add_local_csv(dashboard_path, "sales_final_dataset.csv")

# add the default DateTable to the dashboard 
PBI.add_tmdl_dataset(dashboard_path = dashboard_path, data_path = None, add_default_datetable = True)



# add new page -----------------------------------------------------------------------------------------------------

## page 2 ---------------------------------------------------------------------------------------------------------
# create a new page
PBI.add_new_page(dashboard_path, 
	                   page_name = "Bee Colonies",
	                   title= "The bees are in Trouble!",
	                   subtitle = "We're losing bee colonies"
	)

# uncomment for step two of new page demo
# quit()

# add background image
PBI.add_background_image(dashboard_path = dashboard_path, 
	               page_id = "page2", 
	               img_path = "Taipei_skyline_at_sunset_20150607.jpg", 
	               alpha = 51,
	               scaling_method = "Fit")

## page 3 ------------------------------------------------------------------------------------------------------
PBI.add_new_page(dashboard_path, 
	                   page_name = "Bigfoot Map",
	                   title= "Bigfoot sightings",
	                   subtitle = "By Washington Counties"
	)

## page 4 ------------------------------------------------------------------------------------------------------
PBI.add_new_page(dashboard_path, 
	                   page_name = "Table Page"
	) 

# page 5 ----------------------------------------------------------------------------------------------------------
PBI.add_new_page(dashboard_path, 
	                   page_name = "Table Page 2"
	) 


# Add visual elements ---------------------------------------------------------------------------------------------------

# add a new column chart on the second page
PBI.add_chart(dashboard_path = dashboard_path, 
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

# add a text box to the second page
PBI.add_text_box(text = "Explanatory text in the bottom right corner",
             dashboard_path= dashboard_path,
               page_id = "page2",
                 text_box_id = "page2_explain_box", 
                 height = 200,
                   width= 300,
                     x_position = 1000, 
                     y_position = 600, 
                     font_size = 15)

# add buttons

# download data button (a link to an internet address)
PBI.add_button(label = "Download Data",
  dashboard_path = dashboard_path,
  page_id = "page2",
  button_id = "page2_download_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 540,
  url_link = "https://www.google.com/")

# navigate back to page 1 button
PBI.add_button(label = "Back to page 1",
  dashboard_path = dashboard_path,
  page_id = "page2",
  button_id = "page2_back_to_page1_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 490,
  page_navigation_link = "page1")


## Add a map to page 3 ----------------------------------------------------------------------

PBI.add_shape_map(dashboard_path = dashboard_path, 
              page_id = "page3",
              map_id = "bigfoots_by_county_map",
              data_source = "wa_bigfoot_by_county",
              shape_file_path = "2019_53_WA_Counties9467365124727016.json",
              
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
PBI.add_table(dashboard_path = dashboard_path,
              page_id = "page4", 
              table_id = "sales_table", 
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


PBI.add_sanky_chart(dashboard_path = dashboard_path,
              page_id = "page4", 
              chart_id = "sales_sanky", 
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



PBI.add_sanky_chart(dashboard_path = dashboard_path,
              page_id = "page5", 
              chart_id = "sales_sanky", 
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