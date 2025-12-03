import  os, json, re

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page
from powerbpy.visual import _Visual

class Chart(_Visual):
    """A subset of the visual class, this class represents charts"""

    def __init__(self,
                 page,
                 visual_id,
                 chart_type,
                 data_source,
                 visual_title,
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
        
        visual_id: str
		    Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        chart_type: str
		    The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
        data_source: str
		    The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
        visual_title: str
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
				  visual_title, 
				  
				  height, 
				  width,
				  x_position, 
				  y_position, 
				
				  z_position, 
				  tab_order, 
			      parent_group_id,
				  alt_text)

        # Update the visual type
        self.visual_json["visual"]["visualType"] = chart_type

        # add chart specific sections to the json ------------------------------------------------
            
        ## query -----
        self.visual_json["visual"]["query"] =  {
			"queryState": {
				"Category": {
					"projections": [
						{
							"field": {
								"Column": {
									"Expression": {
										"SourceRef": {
											"Entity": data_source
										}
									},
									"Property": x_axis_var
								}
							},
							"queryRef": f"{data_source}.{x_axis_var}",
							"nativeQueryRef": x_axis_var,
							"active": True
						}
					]
				},
				"Y": {
					"projections": [
						{
							"field": {
								"Aggregation": {
									"Expression": {
										"Column": {
											"Expression": {
												"SourceRef": {
													"Entity": data_source
												}
											},
											"Property": y_axis_var
										}
									},
									"Function": 0
								}
							},
							"queryRef": f"{y_axis_var_aggregation_type}({data_source}.{y_axis_var})",
							"nativeQueryRef": f"{y_axis_var_aggregation_type} of {y_axis_var}"
						}
					]
				}
			},
			"sortDefinition": {
				"sort": [
					{
						"field": {
							"Aggregation": {
								"Expression": {
									"Column": {
										"Expression": {
											"SourceRef": {
												"Entity": data_source
											}
										},
										"Property": y_axis_var
									}
								},
								"Function": 0
							}
						},
						"direction": "Descending"
					}
				],
				"isDefaultSort": True
			}
        }
        
		## objects
        self.visual_json["visual"]["objects"]["categoryAxis"] = [
				{
					"properties": {
						"titleText": {
							"expr": {
								"Literal": {
									"Value": f"'{x_axis_title}'"
								}
							}
						}
					}
				}
		]
            
        self.visual_json["visual"]["objects"]["valueAxis"] = [
				{
					"properties": {
						"titleText": {
							"expr": {
								"Literal": {
									"Value": f"'{y_axis_title}'"
								}
							}
						}
					}
				}
		]

        # Write out the new json 
        with open(self.visual_json_path, "w") as file:
            json.dump(self.visual_json, file, indent = 2)


            
        