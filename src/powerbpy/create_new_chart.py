
import os, json


# , chart_type

def add_chart(dashboard_path,
              page_id, 
              chart_id, 
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
              z_position = 6000 ):


  '''This function adds a new chart to a page in a power BI dashboard report. 


  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the background image to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str chart_id: Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
  
  :param str chart_type: The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
  :param str data_source: The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
  
  :param str chart_title: Give your chart an informative title!:D
  :param str x_axis_title: Text to display on the x axis
  :param str y_axis_title: Text to display on the y axis

  :param str x_axis_var: Column name of a column from data_source that you want to use for the x axis of the chart
  :param str y_axis_var: Column name of a column from data_source that you want to use for the y axis of the chart
  :param str y_axis_var_aggregation_type: Type of aggregation method you want to use to summarize y axis variable. Available options include" ["Sum", "Count", "Average"]
  
  :param int x_position: The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
  :param int y_position: The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.

  
  :param int height: Height of chart on the page
  :param int width: Width of chart on the page

  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000


  '''

  # file paths -------------------------------
  report_name = os.path.basename(dashboard_path)

  pages_folder = os.path.join(dashboard_path, f'{report_name}.Report/definition/pages')
  page_folder_path = os.path.join(pages_folder, page_id)

  visuals_folder = os.path.join(page_folder_path, "visuals")
  new_visual_folder = os.path.join(visuals_folder, chart_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")







	# checks ---------------------------------------------------------

	# page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")

	# chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that chart_id already exists! Try using a different chart_id')

  else: 
    os.makedirs(new_visual_folder)



	# define the json for the new chart
  chart_json = {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
  "name": chart_id,
  "position": {
    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width,
    "tabOrder": tab_order,
  },
  "visual": {
    "visualType": chart_type,
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
    },
    "objects": {
      "categoryAxis": [
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
      ],
      "valueAxis": [
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
    },
    "visualContainerObjects": {
      "title": [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": f"'{chart_title}'"
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

	# Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(chart_json, file, indent = 2)


