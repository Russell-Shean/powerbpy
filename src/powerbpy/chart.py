import  os, json, re

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page

class Chart(Visual):
    """A subset of the visual class, this class represents charts"""

    def __init__(self,
                 page,
                 visual_id,
                 chart_type,
                 data_source,
                 chart_title,
                 x_axis_title,
                 y_axis_title,
                 x_axis_var,
                 y_axis_var,
                 y_axis_var_aggregation_type,
                 x_position,
                 y_position,
                 height,
                 width,
                 tab_order = -1001,
                 z_position = 6000, 
			     parent_group_id = None,
				 alt_text="A chart"):

        '''This function adds a new chart to a page in a power BI dashboard report. 
        Parameters
        ----------
        
        dashboard_path: str
		    The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
        page_id: str
		    The unique id for the page you want to add the background image to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
        chart_id: str
		    Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        chart_type: str
		    The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
        data_source: str
		    The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
        chart_title: str
		    Give your chart an informative title!:D
        x_axis_title: str
		    Text to display on the x axis
        y_axis_title: str
		    Text to display on the y axis
        x_axis_var: str
		    Column name of a column from data_source that you want to use for the x axis of the chart
        y_axis_var: str
		    Column name of a column from data_source that you want to use for the y axis of the chart
        y_axis_var_aggregation_type: str
		    Type of aggregation method you want to use to summarize y axis variable. Available options include" ["Sum", "Count", "Average"]
        x_position: int
		    The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        y_position: int
		    The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        height: int
		    Height of chart on the page
        width: int
		    Width of chart on the page
        tab_order: int
		    The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
		    The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        '''

        super().__init__(page, 
				  visual_id, 

				  data_source, 
				  visual_title, 
				  
				  height, 
				  width,
				  x_position, 
				  y_position, 
				
				  z_position = 6000, 
				  tab_order=-1001, 
			      parent_group_id = None,
				  alt_text="A chart"):
            
            
         