import  os, json, re

def add_card(data_source, 
             measure_name, 
			 dashboard_path, 
			 page_id, 
			 card_id, 
			 height, 
			 width,
			 x_position, 
			 y_position, 
			 z_position = 6000, 
			 tab_order=-1001,
			 title = None,
			 text_align = "left", 
			 font_weight = "bold", 
			 font_size=32, 
			 font_color="#000000", 
			 background_color = None, 
			 parent_group_id = None):
		
	'''Add a card to a page
	
	Parameters
	----------
	data_source: str
		This is the name of the dataset that you want to use to populate the card with
	measure_name: str
		This is the name of the measure (or variable) name you want to use to populate the card with
	dashboard_path: str
		The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
	page_id: str
		The unique id for the page you want to add the card to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
	card_id: str
		Please choose a unique id to use to identify the card. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
	height: int
		Height of card on the page
	width: int
		Width of card on the page
	x_position: int
		The x coordinate of where you want to put the card on the page. Origin is page's top left corner. 
	y_position: int
		The y coordinate of where you want to put the card on the page. Origin is page's top left corner.
	z_position: int
		The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
	tab_order: int
		The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
	title: int 
		An optional title to add to the card. 
	text_align: str
		How would you like the text aligned (available options: "left", "right", "center")
	font_weight: str
		This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
	font_size: int
		The font size in pts. Must be a whole integer. Defaults to 32 pt
	font_color: str
		Hex code for the font color you'd like to use. Defaults to black (#000000) 
	background_color: str
		Hex code for the background color of the card. Defaults to None (transparent)
	parent_group_id: str
		This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group. 
 
	Notes
	-----
	This function creates a new card on a page. 
	'''
	
	# checks --------------------------------------------------------------------------------------------------------------
	# file paths -------------------------------
	# Convert dashboard path to an absolute path if a relative path was provided
	dashboard_path = os.path.abspath(os.path.expanduser(dashboard_path))
	
	report_name = os.path.basename(dashboard_path)
		
	pages_folder = os.path.join(dashboard_path, f'{report_name}.Report/definition/pages')
	page_folder_path = os.path.join(pages_folder, page_id)
		
	visuals_folder = os.path.join(page_folder_path, "visuals")
	new_visual_folder = os.path.join(visuals_folder, card_id)
	visual_json_path = os.path.join(new_visual_folder, "visual.json")

	# checks ---------------------------------------------------------

	# page exists? 
	if os.path.isdir(page_folder_path) is not True:
		raise NameError(f"Couldn't find the page folder at {page_folder_path}")
		
	# chart id unique? 
	if os.path.isdir(new_visual_folder) is True:
		raise ValueError(f'A visual with that card_id already exists! Try using a different card_id')
		
	else: 
		os.makedirs(new_visual_folder)


	card_json = {
	"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
	"name": card_id,
	"position": {
		"x": x_position,
		"y": y_position,
		"z": z_position,
		"height": height,
		"width": width,
		"tabOrder": tab_order
	},
	"visual": {
		"visualType": "card",
		"query": {
			"queryState": {
				"Values": {
					"projections": [
						{
							"field": {
								"Measure": {
									"Expression": {
										"SourceRef": {
											"Entity": data_source
										}
									},
									"Property": measure_name
								}
							},
							"queryRef": f"{data_source}.{measure_name}",
							"nativeQueryRef": measure_name
						}
					]
				}
			},
			"sortDefinition": {
				"isDefaultSort": True
			}
		},
		"objects": {
			"categoryLabels": [
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
			],
			"labels": [
				{
					"properties": {
						"fontSize": {
							"expr": {
								"Literal": {
									"Value": f"{font_size}D"
								}
							}
						},
						"fontFamily": {
							"expr": {
								"Literal": {
									"Value": "'''Segoe UI'', wf_segoe-ui_normal, helvetica, arial, sans-serif'"
								}
							}
						},
						font_weight: {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						},

						"color": {
							"solid": {
								"color": {
									"expr": {
										"Literal": {
											"Value": f"'{font_color}'"
									 
										}
									}
								}
							}
						}
					}
				}
			]
		},
		"visualContainerObjects": {
			"background": [
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
				
			],
			"visualHeader": [
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
			],
			"title": [
				{
					"properties": {
						"text": {
							"expr": {
								"Literal": {
									"Value": f"'{title}'"
								}
							}
						}
					}
				}
			]
		},
		"drillFilterOtherVisuals": True
	}
}
	
	# add the parent group id if the user supplies one
	if parent_group_id is not None:
		card_json["parentGroupName"] = parent_group_id
	

	# add a background color if the user provided one
	if background_color is not None:
		card_json["visual"]["visualContainerObjects"]["background"].append( {
					"properties": {
						"show": {
							"expr": {
								"Literal": {
									"Value": "true"
								}
							}
						}
					}
				})

		card_json["visual"]["visualContainerObjects"]["background"].append( {
					"properties": {
						"color": {
							"solid": {
								"color": {
									"expr": {
										"Literal": {
											"Value": f"'{background_color}'"
										}
									}
								}
							}
						},
						"transparency": {
							"expr": {
								"Literal": {
									"Value": "0D"
								}
							}
						}
					}
				})




	# Write out the new json 
	with open(visual_json_path, "w") as file:
		json.dump(card_json, file, indent = 2)


