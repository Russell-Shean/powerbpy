import  os, json, re

def add_slicer(data_source, column_name, dashboard_path, page_id, slicer_id, height, width,
 x_position, y_position, z_position = 6000, tab_order=-1001,
 title = None,
 text_align = "left", 
  font_weight = "bold", font_size=32, font_color="#000000", background_color = None, parent_group_id = None):
    
  '''Add a slicer to a page

  :param str data_source: This is the name of the dataset that you want to use to populate the slicer with
  :param str column_name: This is the name of the measure (or variable) name you want to use to populate the slicer with
  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the slicer to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str slicer_id: Please choose a unique id to use to identify the slicer. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.

  :param int height: Height of slicer on the page
  :param int width: Width of slicer on the page
 
  :param int x_position: The x coordinate of where you want to put the slicer on the page. Origin is page's top left corner. 
  :param int y_position: The y coordinate of where you want to put the slicer on the page. Origin is page's top left corner.
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
  
  :param str title: An optional title to add to the slicer. 
  :param str text_align: How would you like the text aligned (available options: "left", "right", "center")
  :param str font_weight: This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
  :param int font_size: The font size in pts. Must be a whole integer. Defaults to 32 pt
  :param str font_color: Hex code for the font color you'd like to use. Defaults to black (#000000) 
  :param str background_color: Hex code for the background color of the slicer. Defaults to None (transparent)
  :param str parent_group_id: This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group. 
 

  This function creates a new slicer on a page. 
  '''

  # checks --------------------------------------------------------------------------------------------------------------

  # hex code
  # source: https://gist.github.com/dmartin4820/a53e18871d9490277b26ce21fd191af5
  #hex_match = re.search("/^#?([0-9a-f]{6}|[0-9a-f]{3});$/", font_color)

  #if hex_match is None:
    #raise ValueError("The hex code you provided for the font_color appears to be invalid! Please double check it.")

    
  # file paths -------------------------------
  report_name = os.path.basename(dashboard_path)
    
  pages_folder = os.path.join(dashboard_path, f'{report_name}.Report/definition/pages')
  page_folder_path = os.path.join(pages_folder, page_id)
    
  visuals_folder = os.path.join(page_folder_path, "visuals")
  new_visual_folder = os.path.join(visuals_folder, slicer_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")

  # checks ---------------------------------------------------------

  # page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")
    
  # chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that slicer_id already exists! Try using a different slicer_id')
    
  else: 
    os.makedirs(new_visual_folder)


  slicer_json = {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
  "name": "b6cd7facd60de099c052",
  "position": {
    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width,
    "tabOrder": tab_order},
  "visual": {
    "visualType": "slicer",
    "query": {
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
    },
    "objects": {
      "data": [
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
      ],
      "general": [
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
      ],
      "selection": [
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
    },
    "drillFilterOtherVisuals": True
  }
}
  
  # add the parent group id if the user supplies one
  if parent_group_id is not None:
    slicer_json["parentGroupName"] = parent_group_id
        
  




  # Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(slicer_json, file, indent = 2)



