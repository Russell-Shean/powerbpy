
import os, json


# , chart_type

def add_table(dashboard_path,
              page_id, 
              table_id, 
              data_source, 
              variables,
              x_position, 
              y_position, 
              height, 
              width,
              add_totals_row = False,
              table_title = None,
              column_widths = None,
              tab_order = -1001,
              z_position = 6000 ):

  '''This function adds a new chart to a page in a power BI dashboard report. 

  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the background image to. If you used this package's functions to create pages it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str chart_id: Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
  
  :param str data_source: The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
  :param list variables: The variables from the table that you want to include

  :param str table_title: Give your table an informative title!:D

  :param dict column_widths: Optional. Provide the width of columns. Provide the widths as a dictionary with column names as keys and widths as values. 
  :param int x_position: The x coordinate of where you want to put the table on the page. Origin is page's top left corner.
  :param int y_position: The y coordinate of where you want to put the table on the page. Origin is page's top left corner.

  
  :param int height: Height of table on the page
  :param int width: Width of table on the page

  :param int tab_order: The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
  :param int z_position: The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

  '''

  # file paths -------------------------------
  report_name = os.path.basename(dashboard_path)

  pages_folder = os.path.join(dashboard_path, f'{report_name}.Report/definition/pages')
  page_folder_path = os.path.join(pages_folder, page_id)

  visuals_folder = os.path.join(page_folder_path, "visuals")
  new_visual_folder = os.path.join(visuals_folder, table_id)
  visual_json_path = os.path.join(new_visual_folder, "visual.json")







	# checks ---------------------------------------------------------

	# page exists? 
  if os.path.isdir(page_folder_path) is not True:
    raise NameError(f"Couldn't find the page folder at {page_folder_path}")

	# chart id unique? 
  if os.path.isdir(new_visual_folder) is True:
    raise ValueError(f'A visual with that chart_id already exists! Try using a different table_id')

  else: 
    os.makedirs(new_visual_folder)



	# define the json for the new chart
  table_json = {

  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",

  "name": "e6a4d73607f586bd2f8b",

  "position": {

    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width

  },

  "visual": {
    "visualType": "tableEx",
    "query": {
      "queryState": {
        "Values": {
          "projections": []
        }
      }
    },

    "objects": {

      "columnWidth": [],


      "total": [
        {
          "properties": {
            "totals": {
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

    "visualContainerObjects": {

      "title": []

    },

    "drillFilterOtherVisuals": True

  }


  }


  # loop through the variables and add them to the json
  for variable in variables:

    # Add to the visual bit
    table_json["visual"]["query"]["queryState"]["Values"]["projections"].append(

         
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": data_source
                    }
                  },
                  "Property": variable
                }
              },
              "queryRef": f"{data_source}.{variable}",
              "nativeQueryRef": variable
            }

      )
    
    
  # Adjust column widths if provided
  if column_widths:
    for col_name, col_width in column_widths.items():
      for col_width_entry in table_json.get("visual", {}) \
                                 .get("objects", {}) \
                                 .get("columnWidth", []):
        
        col_width_entry.append(

        {
          "properties": {
            "value": {
              "expr": {
                "Literal": {
                  "Value": f"{col_width}D"
                }
              }
            }
          },
          "selector": {
            "metadata": f"{data_source}.{col_name}"
          }
        }

      )
        
  # Add a totals row if the user asks for it
  if add_totals_row is True:
    for total_entry in table_json.get("visual", {}) \
                                 .get("objects", {}) \
                                 .get("total", []):
        
      total_entry["properties"]["totals"]["expr"]["Literal"]["Value"] = "true"
      
      
  # add a table title if the user asks for it
  if table_title is not None:
    table_json["visual"]["visualContainerObjects"]["title"].append(


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
                  "Value": f"'{table_title}'"
                }
              }
            }


          }

        }





    )
        






	# Write out the new json 
  with open(visual_json_path, "w") as file:
    json.dump(table_json, file, indent = 2)


