
#### --------------------------------------------------------------------------------------------------------------------------------------

import  os, json, re, shutil, uuid

import powerbpy as PBI

def add_shape_map(dashboard_path, page_id, map_id, data_source, shape_file_path,
 map_title, location_var, color_var, color_palette, 
 height, width,
 x_position, y_position, 
 add_legend = True, static_bin_breaks = None, percentile_bin_breaks = None, 
 filtering_var = None,

 z_position = 6000, tab_order=-1001):
    
  '''Add a map to a page

  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the map to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str map_id: Please choose a unique id to use to identify the map. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.

  :param str data_source: The name of the dataset you want to use to build the map. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
  :param str shape_file_path: A path to a shapefile that you want to use to build the map. This shape file will be added to the registered resources.

  :param str map_title: The title you want to put above the map.
  :param str location_var: The name of the column in data_source that you want to use for the location variable on the map
  :param str color_var: The name of the column in data_source that you want to use for the color variable on the map
  :param str filtering_var: Optional. The name of a column in data source that you want to use to filter the color variable on the map. This must be supplied if providing percentile_bin_breaks. If you want to use percentiles without filtering (ie on static data), you should calculate the percentiles yourself and pass them to static_bin_breaks. Do not provide both static_bin_breaks and a filtering_var. 


  :param list static_bin_breaks: This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. A filtering_var cannot be provided if static_bin_breaks is provided. Use percentile bin breaks instead. 
  :param list color_palatte: A list of hex codes to use to color your data. There should be one fewer than the number of entries in static_bin_breaks
  :param bool add_legend: True or False, would you like to add the default legend? (By default legend, I mean this function's default, not the Power BI default)
  :param list static_bin_breaks: This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. 
  :param list percentile_bin_breaks: This should be a list of percentiles between 0 and 1 that you want to us to create bins in your data. If provided, a filtering_var must also be provided. This will create power BI measures that dynamically update when the data is filtered by things such as slicers. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. Here's an example use case: to create 5 equal sized bins pass this list: [0,0.2,0.4,0.6,0.8,1]

  :param int height: Height of map on the page
  :param int width: Width of map on the page
 
  :param int x_position: The x coordinate of where you want to put the map on the page. Origin is page's top left corner. 
  :param int y_position: The y coordinate of where you want to put the map on the page. Origin is page's top left corner.
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
    
    
   


  This function creates a new cloropleth map on a page. 
  '''

  # checks --------------------------------------------------------------------------------------------------------------
  if type(color_palette) is not list: 
        raise TypeError("color_palette should be a list! Please pass a list of hex codes")


  if percentile_bin_breaks is not None and filtering_var is None:
    raise ValueError("You must provide a filtering_var when using percentile_bin_breaks. If you want percentile breaks on static data, calculate percentiles in python and then pass them to static_bin_breaks")

  if percentile_bin_breaks is None and filtering_var is not None:
    raise ValueError("You can't provide a filtering_var if percentile_bin_breaks is not provided")



  if percentile_bin_breaks is None and static_bin_breaks is None:
      raise ValueError("You'll need to provide either static_bin_breaks or percentile_bin_breaks. Otherwise Power BI won't know how to color the map")


  if percentile_bin_breaks is not None and static_bin_breaks is not None:
    raise ValueError("You can't add static and percentile bins to the same map! Please only provide either static_bin_breaks OR percentile_bin_breaks")

    if static_bin_breaks is not None:

      if type(static_bin_breaks) is not list: 
        raise TypeError("static_bin_breaks should be a list! Please pass a list of numbers")

      if len(static_bin_breaks) - len(color_palette) != 1:
        raise ValueError("There should be one fewer colors than number of static_bin_breaks! Please make sure you specified one more break than the number of bins you want.")

    if percentile_bin_breaks is not None:

      if type(percentile_bin_breaks) is not list: 
        raise TypeError("percentile_bin_breaks should be a list! Please pass a list of numbers")

      if len(percentile_bin_breaks) - len(color_palette) != 1:
        raise ValueError("There should be one fewer colors than number of percentile_bin_breaks! Please make sure you specified one more break than the number of bins you want.")


  # hex code
  # source: https://gist.github.com/dmartin4820/a53e18871d9490277b26ce21fd191af5
  #hex_match = re.search("/^#?([0-9a-f]{6}|[0-9a-f]{3});$/", font_color)

  #if hex_match is None:
    #raise ValueError("The hex code you provided for the font_color appears to be invalid! Please double check it.")

    
  # file paths -------------------------------
  report_name = os.path.basename(dashboard_path)
  shape_name = os.path.basename(shape_file_path)

  report_folder = os.path.join(dashboard_path, f'{report_name}.Report')
  definitions_folder = os.path.join(report_folder, "definition")
    
  pages_folder = os.path.join(definitions_folder, "pages")
  page_folder_path = os.path.join(pages_folder, page_id)

  report_json_path = os.path.join(definitions_folder, "report.json")
    
  visuals_folder = os.path.join(page_folder_path, "visuals")
  new_visual_folder = os.path.join(visuals_folder, map_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")


  registered_resources_folder = os.path.join(report_folder, "StaticResources/RegisteredResources")

  # This is the location of the image within the dashboard
  registered_shape_path = os.path.join(registered_resources_folder, shape_name)


  # checks ---------------------------------------------------------

	# page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")
    
  # chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that map_id already exists! Try using a different map_id')
    
  else: 
    os.makedirs(new_visual_folder)


  # Upload shape file to dashboard's registered resources ---------------------------------------------------

  # create registered resources folder if it doesn't exist
  if not os.path.exists(registered_resources_folder):
    os.makedirs(registered_resources_folder)

  # move shape file to registered resources folder
  shutil.copy(shape_file_path, registered_shape_path)



  # add new registered resource (the shape file) to report.json ----------------------------------------------
  with open(report_json_path,'r') as file:
    report_json = json.load(file)


  # add the shape file as an item to the registered resources items list
  for dict in report_json["resourcePackages"]:
    if dict["name"] == "RegisteredResources":
      dict["items"].append(
                          {
                                    "name": shape_name,
                                    "path": shape_name,
                                    "type": "ShapeMap"
                                   }   
                              )




   
  # write to file
  with open(report_json_path,'w') as file:
    json.dump(report_json, file, indent = 2)


  # If percentile breaks are provided, calculate the associated measures
  if percentile_bin_breaks is not None:

    # add bin measures to the dataset
    PBI.add_bin_measures(dashboard_path = dashboard_path,
                 dataset_name = data_source,
                  color_var = color_var, 
                  percentile_bin_breaks = percentile_bin_breaks, 
                  color_palette = color_palette,
                  filtering_var = filtering_var,
                  location_var = location_var
                  #data_filtering_condition = {"metric":"adj_rate"}
                  )   


    # shift x position to the right the width of the slicer
    # to make room for the slicer
    x_position = x_position + 160


  # Create the json that defines the map --------------------------------------------------------------   

  map_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
    "name": map_id,
    "position": {
      "x": x_position,
      "y": y_position,
      "z": z_position,
      "height": height,
      "width": width,
      "tabOrder": tab_order
    },
    "visual": {
      "visualType": "shapeMap",
      "query": {
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
                    "Property": location_var
                  }
                },
                "queryRef": f"{data_source}.{location_var}",
                "nativeQueryRef": location_var
              }
            ]
          }
        },
        "sortDefinition": {
          "isDefaultSort": True
        }
      },
      "objects": {
        "dataPoint": [
          {
            "properties": {
              "fillRule": {
                "linearGradient2": {
                  "min": {
                    "color": {
                      "expr": {
                        "Literal": {
                          "Value": "'minColor'"
                        }
                      }
                    }
                  },
                  "max": {
                    "color": {
                      "expr": {
                        "Literal": {
                          "Value": "'maxColor'"
                        }
                      }
                    }
                  },
                  "nullColoringStrategy": {
                    "strategy": {
                      "expr": {
                        "Literal": {
                          "Value": "'asZero'"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        ],
        "shape": [
          {
            "properties": {
              "map": {
                "geoJson": {
                  "type": {
                    "expr": {
                      "Literal": {
                        "Value": "'packaged'"
                      }
                    }
                  },
                  "name": {
                    "expr": {
                      "Literal": {
                        "Value": f"'{shape_name}'"
                      }
                    }
                  },
                  "content": {
                    "expr": {
                      "ResourcePackageItem": {
                        "PackageName": "RegisteredResources",
                        "PackageType": 1,
                        "ItemName": shape_name
                      }
                    }
                  }
                }
              },
              "projectionEnum": {
                "expr": {
                  "Literal": {
                    "Value": "'orthographic'"
                  }
                }
              }
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
                    "Value": f"'{map_title}'"
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


  
  # Add color bins ----------------------------------------------------------
  # create a color scheme json object
  color_scheme = {
            "properties": {
              "fill": {
                "solid": {
                  "color": {
                    "expr": {
                      "Conditional": {
                        "Cases": []
                      }
                    }
                  }
                }
              }
            },
            "selector": {
              "data": [
                {
                  "dataViewWildcard": {
                    "matchingOption": 1
                  }
                }
              ]
            }
          }


  if static_bin_breaks is not None:

    # add each individual color rule
    # loop through the color_palette and static_bin_breaks to create separate dictionaries for each color bin
    for i in range(0,len(color_palette)):
      color_scheme["properties"]["fill"]["solid"]["color"]["expr"]["Conditional"]["Cases"].append(

    {
      "Condition": {
        "And": {
          "Left": {
            "Comparison": {
              "ComparisonKind": 2,
              "Left": {
                "Aggregation": {
                  "Expression": {
                    "Column": {
                      "Expression": {
                        "SourceRef": {
                          "Entity": data_source
                        }
                      },
                      "Property": color_var
                    }
                  },
                  "Function": 0
                }
              },
              "Right": {
                "Literal": {
                  "Value": f"{static_bin_breaks[i]}D"
                }
              }
            }
          },
          "Right": {
            "Comparison": {
              "ComparisonKind": 3,
              "Left": {
                "Aggregation": {
                  "Expression": {
                    "Column": {
                      "Expression": {
                        "SourceRef": {
                          "Entity": data_source
                        }
                      },
                      "Property": color_var
                    }
                  },
                  "Function": 0
                }
              },
              "Right": {
                "Literal": {
                  "Value": f"{static_bin_breaks[i + 1]}D"
                }
              }
            }
          }
        }
      },
      "Value": {
        "Literal": {
          "Value": f"'{color_palette[i]}'"
        }
      }
    })


  # Else condition: They provided prcentile bins
  if percentile_bin_breaks is not None:
    # add each individual color rule
    # loop through the color_palette and static_bin_breaks to create separate dictionaries for each color bin
    for i in range(0,len(color_palette)):
      color_scheme["properties"]["fill"]["solid"]["color"]["expr"]["Conditional"]["Cases"].append(   

        {
                    "Condition": {
                      "Comparison": {
                        "ComparisonKind": 0,
                        "Left": {
                          "Measure": {
                            "Expression": {
                              "SourceRef": {
                                "Entity": data_source
                              }
                            },
                            "Property": "Bin Assignment Measure"
                          }
                        },
                        "Right": {
                          "Literal": {
                            "Value": f"{i +1}D"
                          }
                        }
                      }
                    },
                    "Value": {
                      "Literal": {
                        "Value": f"'{color_palette[i]}'"
                      }
                    }
                  },)


    # Add in the missing data color and condition
    color_scheme["properties"]["fill"]["solid"]["color"]["expr"]["Conditional"]["Cases"].append(    {
                    "Condition": {
                      "Comparison": {
                        "ComparisonKind": 0,
                        "Left": {
                          "Measure": {
                            "Expression": {
                              "SourceRef": {
                                "Entity": data_source
                              }
                            },
                            "Property": "Bin Assignment Measure"
                          }
                        },
                        "Right": {
                          "Literal": {
                            "Value": "0D"
                          }
                        }
                      }
                    },
                    "Value": {
                      "Literal": {
                        "Value": "'#808080'"
                      }
                    }
                  } )





  map_json["visual"]["objects"]["dataPoint"].append(color_scheme)


  # add a slicer ----------------------------------------------------------
  if percentile_bin_breaks is not None:
    PBI.add_slicer(dashboard_path = dashboard_path,
               data_source = data_source,
               column_name = filtering_var,
               page_id = page_id, 
               slicer_id = f"{filtering_var}_slicer", 
               height = height, 
               width = 160,

               # subtract this back from the 160 we added at the beginning
               x_position = x_position - 160,
               y_position = y_position)







  # add a legend ----------------------------------------------------------------------------------------------------------------------



  if add_legend:

    # determine legend length (we'll say 80% of map's width)
    legend_width = width * .8

    # determin width of each box length
    # this will be the legend's wideth divided by the number of bins
    box_width = round(legend_width / len(color_palette))

    # find the x position to put the first box
    legend_x_position =  x_position + (width - legend_width) /2 

    legend_y_position = y_position + height - 17

    legend_height = 34

    
    # create a larger visual element to be the parent for all the legend boxes
    legend_box_folder = os.path.join(visuals_folder, f"{map_id}_legend_box")
    legend_box_path = os.path.join(legend_box_folder, "visual.json")

    os.makedirs(legend_box_folder)

    #legend_box_uuid = str(uuid.uuid4())

    legend_box_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
    "name":f"{map_id}_legend_box",     #legend_box_uuid,                             # f"{map_id}_legend_box",
    "position": {
    "x": legend_x_position,
    "y": legend_y_position,
    "z": z_position + 1000,
    "height": legend_height,
    "width": legend_width,
    "tabOrder": -1
    },
    "visualGroup": {
    "displayName":    "Bins",    #f"{map_id}_legend_box",
    "groupMode": "ScaleMode"
    }}


    with open(legend_box_path, "w") as file:
      json.dump(legend_box_json, file, indent = 2)


    

    # Add a text box for each bin and make a legend that way
    # There has got to be a better way to do this ....lol
    for i in range(0, len(color_palette)):

      # add text box legends for static maps
      if static_bin_breaks is not None:
        PBI.add_text_box(text = f"{static_bin_breaks[i]} - {static_bin_breaks[i + 1]}", 
                   dashboard_path = dashboard_path, 
                   page_id = page_id, 
                   text_box_id = f"{map_id}_legend_box{i + 1}", 
                   height = legend_height, 
                   width = box_width,

                   # Soooo... this is relative to the outer group
                   # NOT the page!
                   # so needs to be y = 0 and x + n box widths
                   x_position = 0 + box_width * i,
                   y_position = 0,

                   # Make sure that the z index is more than the map's z_index
                   z_position =  z_position + 2000,      #z_position + 1,
                   text_align = "center",
                   font_weight = "bold",
                    font_size=12, 
                    font_color="#ffffff" , 
                    background_color = color_palette[i],
                    #parent_group_id = None
                    parent_group_id = f"{map_id}_legend_box"
                    # parent_group_id = legend_box_uuid
                    )

      # Add card legends for non-static maps
      if percentile_bin_breaks is not None:

       # add this measure "Bin 5 Range"
        PBI.add_card(data_source = data_source,
          measure_name = f"Bin {i + 1} Range",
                   dashboard_path = dashboard_path, 
                   page_id = page_id, 
                   card_id = f"{map_id}_legend_box{i + 1}", 
                   height = 34, 
                   width = box_width,
                   x_position = 0 + box_width * i,
                   y_position = 0,
                   tab_order = -1,

                   # Make sure that the z index is more than the map's z_index
                   z_position = 0,         #z_position + 1,
                   text_align = "center",
                   font_weight = "bold",
                    font_size=12, 
                    font_color="#ffffff" , 
                    background_color = color_palette[i],
                    parent_group_id = f"{map_id}_legend_box")










  # Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(map_json, file, indent = 2)



percentile_breaks = [0.0,0.2,0.4,0.6,0.8,1]
color_var = "count"



