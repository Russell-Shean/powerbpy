import  os, json, re

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page
from powerbpy.visual import _Visual

class Slicer(_Visual):
	"""A generic class for slicers"""

	def __init__(self,
				page,
				data_source, 
			   column_name,  
			   visual_id, 
			   height, 
			   width,
			   x_position, 
			   y_position, 
			   z_position, 
			   tab_order,
			   visual_title,
			   text_align, 
			   font_weight, 
			   font_size, 
			   font_color, 
			   background_color,
			   background_color_alpha, 
			   parent_group_id, 
			   alt_text = "A slicer"):

		'''Add a slicer to a page
		
		Parameters
		----------
		data_source: str
			This is the name of the dataset that you want to use to populate the slicer with
		column_name: str
			This is the name of the measure (or variable) name you want to use to populate the slicer with
		visual_id: str
			Please choose a unique id to use to identify the slicer. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
		height: int
			Height of slicer on the page
		width: int
			Width of slicer on the page
		x_position: int
			The x coordinate of where you want to put the slicer on the page. Origin is page's top left corner. 
		y_position: int
			The y coordinate of where you want to put the slicer on the page. Origin is page's top left corner.
		z_position: int
			The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
		tab_order: int
			The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
		visual_title: str
			An optional title to add to the slicer. 
		text_align: str
			How would you like the text aligned (available options: "left", "right", "center")
		font_weight: str
			This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
		font_size: int
			The font size in pts. Must be a whole integer. Defaults to 32 pt
		font_color: str
			Hex code for the font color you'd like to use. Defaults to black (#000000) 
		background_color: str
			Hex code for the background color of the slicer. Defaults to None (transparent)
		parent_group_id: str
			This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group. 
		
		Notes
		------
		This function creates a new slicer on a page. 
		'''

		super().__init__(page=page, 
				  visual_id=visual_id, 
				  visual_title=visual_title, 
				  
				  height=height, 
				  width=width,
				  x_position=x_position, 
				  y_position=y_position, 
				
				  z_position=z_position, 
				  tab_order=tab_order, 
				  parent_group_id=parent_group_id,
				  alt_text=alt_text, 
				  background_color=background_color,
				  background_color_alpha=background_color_alpha)


		# Update the visual type
		self.visual_json["visual"]["visualType"] = "slicer"

		# add chart specific sections to the json ------------------------------------------------

		## query -----
		self.visual_json["visual"]["query"] = {
			"queryState": {
				"Values": {
					"projections": [
						{
							"field": {
								"Column": {
									"Expression": {
										"SourceRef": {
											"Entity": data_source
										}
									},
									"Property": column_name
								}
							},
							"queryRef": f"{data_source}.{column_name}",
							"nativeQueryRef": column_name,
							"active": True
						}
					]
				}
			}
		}

		## objects
		self.visual_json["visual"]["objects"]["data"] = [
				{
					"properties": {
						"mode": {
							"expr": {
								"Literal": {
									"Value": "'Basic'"
								}
							}
						}
					}
				}
			]

		self.visual_json["visual"]["objects"]["general"] = [

			{
					"properties": {
						"orientation": {
							"expr": {
								"Literal": {
									"Value": "1D"
								}
							}
						},
						"filter": {
							"filter": {
								"Version": 2,
								"From": [
									{
										"Name": "w",
										"Entity": data_source,
										"Type": 0
									}
								],
								"Where": [
									{
										"Condition": {
											"In": {
												"Expressions": [
													{
														"Column": {
															"Expression": {
																"SourceRef": {
																	"Source": "w"
																}
															},
															"Property": column_name
														}
													}
												],
												"Values": [
													[
														{
															"Literal": {
																"Value": "'Click on any other button to get rid of this extra button'"
															}
														}
													]
												]
											}
										}
									}
								]
							}
						}
					}
				}



		]

		self.visual_json["visual"]["objects"]["selection"] = [
				{
					"properties": {
						"singleSelect": {
							"expr": {
								"Literal": {
									"Value": "false"
								}
							}
						},
						"strictSingleSelect": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						}
					}
				}
			]
		
		# Write out the new json 
		with open(self.visual_json_path, "w") as file:
			json.dump(self.visual_json, file, indent = 2)

		

