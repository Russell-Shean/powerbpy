import  os, json, re

def add_button(label, dashboard_path, page_id, button_id, height, width,
 x_position, y_position, z_position = 6000, tab_order=-1001, 
 fill_color="#3086C3", alpha=0, url_link = None, page_navigation_link = None):
    
  '''Add a text box to a page

  :param str label: The text you want to display inside the button.
  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the background image to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str button_id: Please choose a unique id to use to identify the button. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.

  :param int height: Height of text box on the page
  :param int width: Width of text box on the page
 
  :param int x_position: The x coordinate of where you want to put the text box on the page. Origin is page's top left corner. 
  :param int y_position: The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
    
  
  :param int fill_color: Hex code for the background (fill) color you'd like to use for the button. Defaults to blue (#3086C3)
  :param int alpha: The transparency of the background image. Must be a whole integer between 1 and 100. Defaults to 0 (100% not transparent)

  :param str url_link: Optional argument. If provided, the button will navigate to this URL. Should be a full, not relative url
  :param str page_navigation_link: Optional argument. If provided the button will navigate to this page in the report. Must be a valid page_id already present in the report.  
 


  This function creates a new button on a page. 
  '''

  # checks --------------------------------------------------------------------------------------------------------------
  if type(alpha) is not int:
    raise TypeError("alpha (the transparency value) must be an integer between 1-100")

  if (alpha > 100) or (alpha < 0):
    raise ValueError("alpha (the transparency value) must be an integer between 1-100")

  # variable type checks
  for var in [height, width, x_position, y_position, z_position, alpha, tab_order]:
    
    # Get the name of the variable from the locals()
    # dis chatgpt's idea, idk....
    var_name = [name for name, value in locals().items() if value is var][0]

    if type(var) is not int:
      raise ValueError(f"Sorry! The {var_name} variable must be an integer. Please confirm you didn't put quotes around a number")

  # make sure they're not trying to make the button do two things at once
  if page_navigation_link is not None and url_link is not None:
    raise ValueError("Sorry you can only supply a url_link OR a page_navigation_link not both. Decide what you want the button to do and try again")

 


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
  new_visual_folder = os.path.join(visuals_folder, button_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")

  # checks ---------------------------------------------------------
  
  # page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")
    
  # chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that button_id already exists! Try using a different button_id')
    
  else: 
    os.makedirs(new_visual_folder)

  if page_navigation_link is not None:
    # make sure the page id used for the page navigation link is a valid page id
    if os.path.isdir(os.path.join(dashboard_path, f'{report_name}.Report/definition/pages/{page_navigation_link}')) is not True:
      raise ValueError("Sorry the page you are trying to link the button to doesn't exist yet. Please confirm the page id or create a new page using the add_new_page() function")
   

    
  button_json = {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
  "name": button_id,
  "position": {
    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width,
    "tabOrder": tab_order
  },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "icon": [
        {
          "properties": {
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
      ],
      "outline": [
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
      "fill": [
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
      ],
      "text": [
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
    },
    "visualContainerObjects": {
      "title": [
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
    },
    "drillFilterOtherVisuals": True
  },
  "howCreated": "InsertVisualButton"
}

  # add a link that the button will open when clicked
  # but only if the user supplied a link
  if url_link is not None:
    button_json["visual"]["visualContainerObjects"]["visualLink"] =  [
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
    button_json["visual"]["visualContainerObjects"]["visualLink"] = [
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
      }
    }
  ]

  

  # Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(button_json, file, indent = 2)


