from powerbpy import *

import os


my_dashboard = Dashboard(os.getcwd(), "test_dashboard")

my_dashboard.new_page(page_name = "Bigfoot Map",
 title= "Bigfoot sightings", 
 subtitle = "By Washington Counties")

