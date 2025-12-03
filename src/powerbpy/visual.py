import  os, json, re

from powerbpy.page import Page

class _Visual:
	def __init__(self,
	             page, 
				#  page_id, 
				  visual_id, 
				  
				  height, 
				  width,
				  x_position, 
				  y_position, 
				  visual_title=None,
				
				  z_position = 6000, 
				  tab_order=-1001, 
				  parent_group_id = None,
				  alt_text="A generic visual"):

		

		self.page = page
		self.dashboard = page.dashboard

		self.visual_id = visual_id
		self.visual_title = visual_title
		self.height = height
		self.width = width
		self.x_position = x_position
		self.y_position = y_position
		self.z_position = z_position
		self.tab_order = tab_order
		self.parent_group_id = parent_group_id
		self.alt_text = alt_text

		# Define generic properties
		self.powerbi_schema = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json"
		self.visual_type = "GENERIC_VISUAL"

		# checks ---------------------------------------------------------

		if not isinstance(page, Page):
			raise TypeError("Visuals must be added to a specific page")
			
		# visual id unique? 
		self.new_visual_folder = os.path.join(self.page.visuals_folder, self.visual_id)
		self.visual_json_path = os.path.join(self.new_visual_folder, "visual.json")

		if os.path.isdir(self.new_visual_folder) is True:
			raise ValueError(f'A visual with that visual_id already exists! Try using a different visual_id')
			
		else: 
			os.makedirs(self.new_visual_folder)


		# Define the generic json for the visual
		# define the json for the new chart
		self.visual_json = {
			"$schema": self.powerbi_schema,
			"name": self.visual_id,
			"position": {
				"x": self.x_position,
				"y": self.y_position,
				"z": self.z_position,
				"height": self.height,
				"width": self.width,
				"tabOrder": self.tab_order,
				},

			"visual": {
				"visualType": self.visual_type,
				"objects": {},
				"visualContainerObjects": {
					"general": [
						{
							"properties": {
								"altText": {
									"expr": {
										"Literal": {
											"Value": f"'{self.alt_text}'"
											}
										}
									}}
									}
								],
					"title": []
					},
				"drillFilterOtherVisuals": True
				
				}
				
		}
		
		# Add a title to the visual if the user provides one
		if self.visual_title is not None:
			self.visual_json["visual"]["visualContainerObjects"]["title"].append(


				{
					"properties": {
						"show": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						},


						"text": {
							"expr": {
								"Literal": {
									"Value": f"'{visual_title}'"
								}
							}
						}


					}

				}
				
			)
				
