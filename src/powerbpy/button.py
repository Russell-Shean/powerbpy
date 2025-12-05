import  os, json, re

from powerbpy.dashboard import Dashboard
from powerbpy.page import Page
from powerbpy.visual import _Visual

class Button(_Visual):
	""" A subset of the Visual class. This represents buttons"""

	def __init__(self,
				 page,
				 label, 
				 visual_id, 
				 height, 
				 width,
				 x_position, 
				 y_position, 
				 z_position = 6000, 
				 tab_order=-1001, 
				 fill_color="#3086C3", 
				 alpha=0, 
				 url_link = None, 
				 page_navigation_link = None ,
				 parent_group_id = None,
				 alt_text = "A button",
				 background_color = None,
				 background_color_alpha= None
				 ):

		'''Add a button to a page
		
		Parameters
		----------
		label : str
		The text you want to display inside the button
		button_id: str
		Please choose a unique id to use to identify the button. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
		height: int
		Height of text box on the page
		width: int
		Width of text box on the page
		x_position: int
		The x coordinate of where you want to put the text box on the page. Origin is page's top left corner.
		y_position: int
		The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
		z_position: int
		The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
		tab_order: int
		The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
		fill_color: str
		Hex code for the background (fill) color you'd like to use for the button. Defaults to blue (#3086C3)
		alpha: int
		The transparency of the fill color. Must be a whole integer between 1 and 100. Defaults to 0 (100% not transparent)
		url_link: str
		Optional argument. If provided, the button will navigate to this URL. Should be a full, not relative url
		page_navigation_link: str
		Optional argument. If provided the button will navigate to this page in the report. Must be a valid page_id already present in the report.
		
		Notes
		-----
		This function creates a new button on a page.
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
				  alt_text=alt_text, 
				  background_color=background_color,
				  background_color_alpha=background_color_alpha)


		# checks --------------------------------------------------------------------------------------------------------------
		if type(alpha) is not int:
			raise TypeError("alpha (the transparency value) must be an integer between 1-100")
			
		if (alpha > 100) or (alpha < 0):
			raise ValueError("alpha (the transparency value) must be an integer between 1-100")
			
		# make sure they're not trying to make the button do two things at once
		if page_navigation_link is not None and url_link is not None:
			raise ValueError("Sorry you can only supply a url_link OR a page_navigation_link not both. Decide what you want the button to do and try again")
		
 
		if page_navigation_link is not None:
			# make sure the page id used for the page navigation link is a valid page id
			if os.path.isdir(os.path.join(self.dashboard.pages_folder, page_navigation_link)) is not True:
				raise ValueError("Sorry the page you are trying to link the button to doesn't exist yet. Please confirm the page id or create a new page using the add_new_page() function")
				
				
		# Update the visual type
		self.visual_json["visual"]["visualType"] = "actionButton"


		## objects
		self.visual_json["visual"]["objects"]["icon"] =  [
			   {"properties": {
				 "shapeType": {
				   "expr": {
								"Literal": {
									"Value": "'blank'"
								}
							}
						}
					},
					"selector": {
						"id": "default"
					}
				}
			]

		self.visual_json["visual"]["objects"]["outline"] = [
				{
					"properties": {
						"show": {
							"expr": {
								"Literal": {
									"Value": "false"
								}
							}
						}
					}
				}
			]

		
		self.visual_json["visual"]["objects"]["fill"] = [
				{
					"properties": {
						"show": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						}
					}
				},
				{
					"properties": {
						"fillColor": {
							"solid": {
								"color": {
									"expr": {
										"Literal": {
											"Value": f"'{fill_color}'"
										}
									}
								}
							}
						},
						"transparency": {
							"expr": {
								"Literal": {
									"Value": f"{alpha}D"
								}
							}
						}
					},
					"selector": {
						"id": "default"
					}
				}
			]


		self.visual_json["visual"]["objects"]["text"] = [
				{
					"properties": {
						"show": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						}
					}
				},
				{
					"properties": {
						"text": {
							"expr": {
								"Literal": {
									"Value": f"'{label}'"
								}
							}
						},
						"fontColor": {
							"solid": {
								"color": {
									"expr": {
										"ThemeDataColor": {
											"ColorId": 0,
											"Percent": 0
										}
									}
								}
							}
						},
						"bold": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						}
					},
					"selector": {
						"id": "default"
					}
				}
			]

		# Visual container object
		self.visual_json["visual"]["visualContainerObjects"]["title"] = [
				{
					"properties": {
						"text": {
							"expr": {
								"Literal": {
									"Value": "'DOWNLOAD'"
								}
							}
						}
					}
				}
			] 

		# add the how created notation
		self.visual_json["howCreated"] = "InsertVisualButton"
		
		# add a link that the button will open when clicked
		# but only if the user supplied a link
		if url_link is not None:
			self.visual_json["visual"]["visualContainerObjects"]["visualLink"] =  [
					{
						"properties": {
							"show": {
								"expr": {
									"Literal": {
										"Value": "true"
									}
								}
							},
							"type": {
								"expr": {
									"Literal": {
										"Value": "'WebUrl'"
									}
								}
							},
							"webUrl": {
								"expr": {
									"Literal": {
										"Value": f"'{url_link}'"
									}
								}
							}
						}
					}
				]
				
		if page_navigation_link is not None:
			self.visual_json["visual"]["visualContainerObjects"]["visualLink"] = [
				{
			"properties": {
				"show": {
					"expr": {
						"Literal": {
							"Value": "true"
						}
					}
				},
				"type": {
					"expr": {
						"Literal": {
							"Value": "'PageNavigation'"
						}
					}
				},
				"navigationSection": {
					"expr": {
						"Literal": {
							"Value": f"'{page_navigation_link}'"
						}
					}
				}
			}}]
			
		# Write out the new json 
		with open(self.visual_json_path, "w") as file:
			json.dump(self.visual_json, file, indent = 2)
