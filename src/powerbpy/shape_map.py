import  os, json, re, shutil, uuid

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page
from powerbpy.visual import _Visual

class ShapeMap(_Visual):
    """ A subclass of the visual class, this represents a shapemap"""

    def __init__(self,
                 page,
				  visual_id, 
				  data_source, 
				  shape_file_path,
				  map_title, 
				  location_var, 
				  color_var,
				  color_palette, 
				  height, 
				  width,
				  x_position, 
				  y_position, 
				  add_legend = True, 
				  static_bin_breaks = None, 
				  percentile_bin_breaks = None, 
				  filtering_var = None,
				  z_position = 6000, 
				  tab_order=-1001,
                  parent_group_id = None,
                 alt_text = "A button"):


        '''Add a map to a page
        ![Example of a shape map created by the function](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/page2.gif?raw=true "Example Shape Map")
        
        Parameters
        ----------
        visual_id: str
		Please choose a unique id to use to identify the map. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        data_source: str
		The name of the dataset you want to use to build the map. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
        shape_file_path: str
		A path to a shapefile that you want to use to build the map. This shape file will be added to the registered resources.
        map_title: str
		The title you want to put above the map.
        location_var: str
		The name of the column in data_source that you want to use for the location variable on the map
        color_var: str
		The name of the column in data_source that you want to use for the color variable on the map
        filtering_var: str
		Optional. The name of a column in data source that you want to use to filter the color variable on the map. This must be supplied if providing percentile_bin_breaks. If you want to use percentiles without filtering (ie on static data), you should calculate the percentiles yourself and pass them to static_bin_breaks. Do not provide both static_bin_breaks and a filtering_var. 
        static_bin_breaks: list
		This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. A filtering_var cannot be provided if static_bin_breaks is provided. Use percentile bin breaks instead. 
        color_palatte: list
		A list of hex codes to use to color your data. There should be one fewer than the number of entries in static_bin_breaks
        add_legend: bool
		True or False, would you like to add the default legend? (By default legend, I mean this function's default, not the Power BI default)
        static_bin_breaks: list
		This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. 
	percentile_bin_breaks: list
		This should be a list of percentiles between 0 and 1 that you want to us to create bins in your data. If provided, a filtering_var must also be provided. This will create power BI measures that dynamically update when the data is filtered by things such as slicers. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. Here's an example use case: to create 5 equal sized bins pass this list: [0,0.2,0.4,0.6,0.8,1]
	height: int
		Height of map on the page
	width: int
		Width of map on the page
	x_position: int
		The x coordinate of where you want to put the map on the page. Origin is page's top left corner. 
	y_position: int
		The y coordinate of where you want to put the map on the page. Origin is page's top left corner.
	z_position: int
		The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
	tab_order: int
		The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
		
	Notes
	-----
	This function creates a new cloropleth map on a page. 
	'''


        super().__init__(page=page, 
				  visual_id=visual_id, 
				  
				  height=height, 
				  width=width,
				  x_position=x_position, 
				  y_position=y_position, 
				
				  z_position=z_position, 
				  tab_order=tab_order, 
			      parent_group_id=parent_group_id,
				  alt_text=alt_text)
