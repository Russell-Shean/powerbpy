import  os, json, re

def add_text_box(text, dashboard_path, page_id, text_box_id, height, width,
 x_position, y_position, z_position = 6000, tab_order=-1001,
 text_align = "left", 
  font_weight = "bold", font_size=32, font_color="#000000", background_color = None, parent_group_id = None):
    
  '''Add a text box to a page

  :param str text: The text you want to display in the box
  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the text box to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str text_box_id: Please choose a unique id to use to identify the text box. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.

  :param int height: Height of text box on the page
  :param int width: Width of text box on the page
 
  :param int x_position: The x coordinate of where you want to put the text box on the page. Origin is page's top left corner. 
  :param int y_position: The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
    
  :param str text_align: How would you like the text aligned (available options: "left", "right", "center")
  :param str font_weight: This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
  :param int font_size: The font size in pts. Must be a whole integer. Defaults to 32 pt
  :param str font_color: Hex code for the font color you'd like to use. Defaults to black (#000000) 
  :param str background_color: Hex code for the background color of the text box. Defaults to None (transparent)
  :param str parent_group_id: This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group. 

  This function creates a new text box on a page. 
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
  new_visual_folder = os.path.join(visuals_folder, text_box_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")

  # checks ---------------------------------------------------------

  # page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")
    
  # chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that text_box_id already exists! Try using a different text_box_id')
    
  else: 
    os.makedirs(new_visual_folder)
        
        
  text_box_json = {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
  "name": text_box_id,
  "position": {
    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width,
    "tabOrder": tab_order 
  },
  "visual": {
    "visualType": "textbox",
    "objects": {
      "general": [
        {
          "properties": {
            "paragraphs": [
              {
                "textRuns": [
                  {
                    "value": text,
                    "textStyle": {
                      "fontWeight": font_weight,
                      "fontSize": f"{font_size}pt",
                      "color": font_color
                    }
                  }
                ],
                "horizontalTextAlignment": text_align
              }
            ]
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
      ]
    },
    "drillFilterOtherVisuals": True
  }
    }



  # add a background color if the user provided one
  if background_color is not None:
    text_box_json["visual"]["visualContainerObjects"]["background"].append( {
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

    text_box_json["visual"]["visualContainerObjects"]["background"].append( {
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

  # add the parent group id if the user supplies one
  if parent_group_id is not None:
    text_box_json["parentGroupName"] = parent_group_id




  # Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(text_box_json, file, indent = 2)


