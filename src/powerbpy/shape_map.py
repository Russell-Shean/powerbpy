""" A subclass of the visual class, this represents a shapemap"""

import os
import json
import shutil
import uuid

from powerbpy.visual import _Visual

class _ShapeMap(_Visual):
    """ A subclass of the visual class, this represents a shapemap"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches, too-many-statements
    # pylint: disable=too-many-arguments, pointless-string-statement
    # pylint: disable=duplicate-code

    def __init__(self,
                 page,
                 *,
                  visual_id,
                  data_source,
                  shape_file_path,
                  map_title,
                  location_var,
                  color_var,
                  color_palette,
                  height,
                  width,
                  x_position,
                  y_position,
                  add_legend = True,
                  static_bin_breaks = None,
                  percentile_bin_breaks = None,
                  filtering_var = None,
                  z_position = 6000,
                  tab_order=-1001,
                  parent_group_id = None,
                 alt_text = "A shape map",
                 background_color=None,
                 background_color_alpha=None):


        '''Add a map to a page
        ![Example of a shape map created by the function](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/page2.gif?raw=true "Example Shape Map")

        Parameters
        ----------
        visual_id: str
            Please choose a unique id to use to identify the map. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        data_source: str
            The name of the dataset you want to use to build the map. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        shape_file_path: str
            A path to a shapefile that you want to use to build the map. This shape file will be added to the registered resources.
        map_title: str
            The title you want to put above the map.
        location_var: str
            The name of the column in data_source that you want to use for the location variable on the map
        color_var: str
            The name of the column in data_source that you want to use for the color variable on the map
        filtering_var: str
            Optional. The name of a column in data source that you want to use to filter the color variable on the map. This must be supplied if providing percentile_bin_breaks. If you want to use percentiles without filtering (ie on static data), you should calculate the percentiles yourself and pass them to static_bin_breaks. Do not provide both static_bin_breaks and a filtering_var.
        static_bin_breaks: list
            This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. A filtering_var cannot be provided if static_bin_breaks is provided. Use percentile bin breaks instead.
        color_palatte: list
            A list of hex codes to use to color your data. There should be one fewer than the number of entries in static_bin_breaks
        add_legend: bool
            True or False, would you like to add the default legend? (By default legend, I mean this function's default, not the Power BI default)
        static_bin_breaks: list
            This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc.
        percentile_bin_breaks: list
            This should be a list of percentiles between 0 and 1 that you want to us to create bins in your data. If provided, a filtering_var must also be provided. This will create power BI measures that dynamically update when the data is filtered by things such as slicers. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. Here's an example use case: to create 5 equal sized bins pass this list: [0,0.2,0.4,0.6,0.8,1]
        height: int
            Height of map on the page
        width: int
            Width of map on the page
        x_position: int
            The x coordinate of where you want to put the map on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the map on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)

        Notes
        -----
        This function creates a new cloropleth map on a page.
        '''

        #self.dashboard = dashboard
        self.page = page
        self.x_position = x_position


        # checks --------------------------------------------------------------------------------------------------------------
        if not isinstance(color_palette, list):
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

            if not isinstance(static_bin_breaks, list):
                raise TypeError("static_bin_breaks should be a list! Please pass a list of numbers")

            if len(static_bin_breaks) - len(color_palette) != 1:
                raise ValueError("There should be one fewer colors than number of static_bin_breaks! Please make sure you specified one more break than the number of bins you want.")

        if percentile_bin_breaks is not None:

            if not isinstance(percentile_bin_breaks, list):
                raise TypeError("percentile_bin_breaks should be a list! Please pass a list of numbers")

            if len(percentile_bin_breaks) - len(color_palette) != 1:
                raise ValueError("There should be one fewer colors than number of percentile_bin_breaks! Please make sure you specified one more break than the number of bins you want.")




        super().__init__(page=page,
                  visual_id=visual_id,
                  visual_title=map_title,

                  height=height,
                  width=width,
                  x_position=self.x_position,
                  y_position=y_position,

                  z_position=z_position,
                  tab_order=tab_order,
                  parent_group_id=parent_group_id,
                  alt_text=alt_text,
                  background_color=background_color,
                  background_color_alpha=background_color_alpha)


        # Upload shape file to dashboard's registered resources ---------------------------------------------------
        # create registered resources folder if it doesn't exist
        if not os.path.exists(self.dashboard.registered_resources_folder):
            os.makedirs(self.dashboard.registered_resources_folder)


        # This is the location of the fhape file within the dashboard
        shape_name = os.path.basename(shape_file_path)

        registered_shape_path = os.path.join(self.dashboard.registered_resources_folder, shape_name)

        # move shape file to registered resources folder
        shutil.copy(shape_file_path, registered_shape_path)

        # add new registered resource (the shape file) to report.json ----------------------------------------------
        with open(self.dashboard.report_json_path,'r', encoding="utf-8") as file:
            report_json = json.load(file)


        # add the shape file as an item to the registered resources items list
        for resource_package in report_json["resourcePackages"]:
            if resource_package["name"] == "RegisteredResources":
                resource_package["items"].append(
                                                    {
                                                                        "name": shape_name,
                                                                        "path": shape_name,
                                                                        "type": "ShapeMap"
                                                                     }
                                                            )


        # write to file
        with open(self.dashboard.report_json_path,'w', encoding="utf-8") as file:
            json.dump(report_json, file, indent = 2)


        # If percentile breaks are provided, calculate the associated measures
        if percentile_bin_breaks is not None:

            # add bin measures to the dataset
            self._add_bin_measures(dataset_name = data_source,
                                    color_var = color_var,
                                    percentile_bin_breaks = percentile_bin_breaks,
                                    #color_palette = color_palette,
                                    #filtering_var = filtering_var,
                                    location_var = location_var
                                    #data_filtering_condition = {"metric":"adj_rate"}
                                    )


            # shift x position to the right the width of the slicer
            # to make room for the slicer
            self.x_position += 160

            self.visual_json["position"]["x"] = self.x_position

        # Create the json that defines the map --------------------------------------------------------------
        # Update the visual type
        self.visual_json["visual"]["visualType"] = "shapeMap"

        ## query -----
        self.visual_json["visual"]["query"] = {
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
            }

        ## objects
        self.visual_json["visual"]["objects"]["dataPoint"] = [
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
                ]

        self.visual_json["visual"]["objects"]["shape"] = [
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
            for i, color in enumerate(color_palette):
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
                            "Value": f"'{color}'"
                            }}
                })

        # Else condition: They provided prcentile bins
        if percentile_bin_breaks is not None:
            # add each individual color rule
            # loop through the color_palette and static_bin_breaks to create separate dictionaries for each color bin
            for i, color in enumerate(color_palette):
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
                                                "Value": f"'{color}'"
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

        self.visual_json["visual"]["objects"]["dataPoint"].append(color_scheme)

        # add a slicer ----------------------------------------------------------
        if percentile_bin_breaks is not None:
            self.page.add_slicer(data_source = data_source,
                             column_name = filtering_var,
                             visual_id = f"{filtering_var}_slicer",
                             height = height,
                             width = 160,

                             # subtract this back from the 160 we added at the beginning
                             x_position = self.x_position - 160,
                             y_position = y_position,
                             alt_text = f"Map legend for the {visual_id} map")


        # add a legend ----------------------------------------------------------------------------------------------------------------------
        if add_legend:

            # determine legend length (we'll say 80% of map's width)
            legend_width = width * .8

            # determine width of each box length
            # this will be the legend's wideth divided by the number of bins
            box_width = round(legend_width / len(color_palette))

            # find the x position to put the first box
            legend_x_position =  self.x_position + (width - legend_width) /2

            legend_y_position = y_position + height - 17

            legend_height = 34

            # create a larger visual element to be the parent for all the legend boxes
            legend_box_folder = os.path.join(self.page.visuals_folder, f"{visual_id}_legend_box")
            legend_box_path = os.path.join(legend_box_folder, "visual.json")

            os.makedirs(legend_box_folder)

            #legend_box_uuid = str(uuid.uuid4())

            legend_box_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json",
                "name":f"{visual_id}_legend_box",     #legend_box_uuid,                             # f"{map_id}_legend_box",
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

            with open(legend_box_path, "w", encoding="utf-8") as file:
                json.dump(legend_box_json, file, indent = 2)

            # Add a text box for each bin and make a legend that way
            # There has got to be a better way to do this ....lol
            #for i in enumerate(color_palette):
            
            # pylint: disable=consider-using-enumerate
            for i in range(0, len(color_palette)):

                # add text box legends for static maps
                if static_bin_breaks is not None:
                    self.page.add_text_box(text = f"{static_bin_breaks[i]} - {static_bin_breaks[i + 1]}",
                                     text_box_id = f"{visual_id}_legend_box{i + 1}",
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
                                        parent_group_id = f"{visual_id}_legend_box"
                                        # parent_group_id = legend_box_uuid
                                        )

                # Add card legends for non-static maps
                if percentile_bin_breaks is not None:

                    # add this measure "Bin 5 Range"
                    self.page.add_card(data_source = data_source,
                                     measure_name = f"Bin {i + 1} Range",
                                     visual_id = f"{visual_id}_legend_box{i + 1}",
                                     height = 34,
                                     width = box_width,
                                     x_position = 0 + box_width * i,
                                     y_position = 0,
                                     tab_order = -1,

                                     # Make sure that the z index is more than the map's z_index
                                     z_position = 0,         #z_position + 1,
                                     #text_align = "center",
                                     font_weight = "bold",
                                        font_size=12,
                                        font_color="#ffffff" ,
                                        background_color = color_palette[i],
                                        parent_group_id = f"{visual_id}_legend_box")


        # Write out the new json
        with open(self.visual_json_path, "w", encoding="utf-8") as file:
            json.dump(self.visual_json, file, indent = 2)



    def _generate_bin_ranges(self,
                             *,
                             bin_number,
                                                 dataset_file_path,
                                                 percentile_bin_breaks,
                                                 dataset_name,
                                                 color_var,
                                                 location_var,
                                                 filtering_dax):

        '''An internal function for creating bins within the _add_bin_measures() function

        Parameters
        ----------
        bin_number: int
            The number of the bin being created

        Notes
        -----
        from the original DAX
        /*
        Step 1: Calculate the percentiles again (same as Bin Assignment Measure)

        Note that since the boundaries of the higher bins refer to those of the lower bins,
        you need to make sure that all previous percentile calculations and bin boundaries are also calculated for each range.
        Here is the final (fifth) bin range measure and it requires all percentiles and bin boundaries to create the range of the fifth bin.
        */


        /*
        Step 2: Calculate the bin boundaries again (same as Bin Assignment Measure)
        */

        /*
        Step 3: Format the bin boundaries as desired to display in a card visual (output of the measure).
        */

        '''
        with open(dataset_file_path, 'a', encoding="utf-8") as file:
            file.write(f"\tmeasure 'Bin {bin_number} Range' =\n")

            for i in range(0, bin_number):

                if i == 0:
                    file.write(f'\t\t\tVAR perc_{round(percentile_bin_breaks[i] * 100)} =  CALCULATE ( PERCENTILE.INC ({dataset_name}[{color_var}], {percentile_bin_breaks[i]} ), REMOVEFILTERS({dataset_name}[{location_var}]){filtering_dax} )\n')
                    file.write(f'\t\t\tVAR perc_{round(percentile_bin_breaks[i +1] * 100)} = CALCULATE ( PERCENTILE.INC ({dataset_name}[{color_var}], {percentile_bin_breaks[i+1]} ), REMOVEFILTERS({dataset_name}[{location_var}]){filtering_dax}  )\n')

                else:
                    file.write(f'\t\t\tVAR perc_{round(percentile_bin_breaks[i +1] * 100)} = CALCULATE ( PERCENTILE.INC ({dataset_name}[{color_var}], {percentile_bin_breaks[i+1]} ), REMOVEFILTERS({dataset_name}[{location_var}]){filtering_dax}  )\n')

            for i in range(0,bin_number):

                if i == 0:
                    file.write(f'\t\t\tVAR bin{i +1}_LB = perc_{round(percentile_bin_breaks[i] * 100)}')
                    file.write(f'\t\t\tVAR bin{i +1}_UB = IF ( perc_{round(percentile_bin_breaks[i] * 100)} == perc_{round(percentile_bin_breaks[i+1] * 100)}, bin{i+1}_LB + 0.01, ROUND( perc_{round(percentile_bin_breaks[i+1] * 100)}, 2) )\n')

                else:
                    file.write(f'\t\t\tVAR bin{i +1}_LB = bin{i}_UB + 0.01\n' )
                    file.write(f'\t\t\tVAR bin{i+1}_UB = IF ( perc_{round(percentile_bin_breaks[i] * 100)} == perc_{round(percentile_bin_breaks[i + 1] * 100)} || perc_{round(percentile_bin_breaks[i + 1] * 100)} <= bin{i + 1}_LB, bin{i+1}_LB + 0.01, ROUND( perc_{round(percentile_bin_breaks[i + 1] * 100)}, 2) )\n')

            file.write("\t\t\tRETURN\n")
            file.write(f'\t\t\tbin{bin_number}_LB & "-" & bin{bin_number}_UB\n')
            file.write(f'\t\tlineageTag: {str(uuid.uuid4())}\n')


    # pylint: disable=too-many-arguments, pointless-string-statement
    def _add_bin_measures(self,
                         *,
                     dataset_name,
                     color_var,
                     percentile_bin_breaks,
                     #color_palette,
                     #filtering_var,
                     location_var,
                     data_filtering_condition = None):

        '''An internally called function that adds bin measures to a TMDL file

        Parameters
        ----------
        dashboard_path: str
            The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders).
        dataset_name: str
            The name of the dataset. This should be the basename of the original file without the extension. For example if you loaded "%userprofile%/documents/datasets/birds.csv", the dataset name would be "birds".
        dataset_id: str
            The dataset's UUID, this will be generated by the outer level function that calls create_tmdl().
        dataset: DataFrame
            This is a pandas dataframe of the csv's content. The pd.read_csv() function is called by the outer level function that calls create_tmdl().
        data_filtering_condition: dict
            This is a key value pair for filtering long data. The key should be the column you want to look for and the value should be the value in that column that you want to filter for.For example if the original data has a column called metric with a variety of different metrics and you want to filter the dataset for only rows where the column is equal to "adj_rate", you should provide the following {"metric":"adj_rate"}

        Returns
        -------
        col_attributes: dict
            A dictionary containing the name and type of all the columns in the dataset. This is needed to get the M code in the outer level function to work.

        Notes
        -----
        This function loops through all the dataframe's columns, checks the column's type (text, number, date), and generates the appropriate TMDL column definition for that type.
        Dates will only be recocognized as dates if they are in the format (YYYY-MM-DD) i.e. (1999-12-31). If your date is in another format please change in python before calling the add_csv functions.

        '''

        # checks
        if max(percentile_bin_breaks) > 1 or min(percentile_bin_breaks) < 0:
            raise ValueError("Sorry the percentile_bin_breaks should express decimal percentiles between 0 and 1. For example the 20th percentile should be written as 0.2")

        # If a data_filtering_condition argument was provided, make sure it's a dictionary with only a single key-value pair
        if data_filtering_condition is not None:

            if (
                not isinstance(data_filtering_condition, dict)
                or len(data_filtering_condition) != 1
                or not all(isinstance(k, str) for k in data_filtering_condition.keys())):

                raise TypeError(
                    "data_filtering_condition must be a dict with exactly one string key. "
                    "Example: {'metric': 'adj_rate'}"
                    )

        # file paths ---------------------------------------------------------------------------

        dataset_file_path = os.path.join(self.dashboard.tables_folder, f'{dataset_name}.tmdl')

        #check to make sure the dataset exists
        if not os.path.exists(dataset_file_path):
            raise ValueError("The {dataset_name} dataset doesn't exist yet! Try adding it using Dashboard.add_local_csv() or one of the other methods for adding datasets")



        # define a DAX statement for filtering the data
        # If a dictionary was provided, we'll convert it to DAX
        # otherwise the variable will = ""
        if data_filtering_condition is None:
            filtering_dax = ""

        else:
            for column, value in data_filtering_condition.items():
                filtering_dax = f', {dataset_name}[{column}] == "{value}"'


        # append a new measure for the total to the dataset
        with open(dataset_file_path, 'a', encoding="utf-8") as file:
            #file.write("\n\n --------------   Begin auto generated stuff -------------------\n\n")
            file.write(f"\tmeasure 'Measure Value' = CALCULATE ( SUM ( {dataset_name}[{color_var}]{filtering_dax} ))\n")
            file.write(f'\t\tlineageTag: {str(uuid.uuid4())}\n')
            file.write('\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}\n\n')

            # Notes taken from the original DAX:
            '''
                    /* Step 1: Calculate the percentiles for the displayed data

            Note that this measure relies on raw values existing in the back-end data or PBI virtual table, not values that come from calculations
            done within the PBI dataset via measure. It may not be possible to consider all the values given by a measure for each county as a set
            from which percentiles can be calculated. At least I haven’t been successful at this.

            On a map visual, we are “selecting” a specific county when we hover the mouse over a particular area.
            We want to make sure we are calculating the percentiles based on all available counties.
             Here, I chose REMOVEFILTERS() to make sure that the entire set of values is considered when calculating the percentiles.
             Without this, the set being used for the calculation would just consist of the single value of the hovered-on county.

            For quintile calculations, calculate the 0th, 20th, 40th, 60th, 80th, and 100th percentiles for the data.
            This will allow you to create five bins

            */
            '''
            # start adding quintiles
            file.write("\tmeasure 'Bin Assignment Measure' = ```\n\n")

            for percentile in percentile_bin_breaks:
                file.write(f"\t\t VAR perc_{round(percentile * 100)} = \n")
                file.write(f'\t\t\t\tCALCULATE ( PERCENTILE.INC ({dataset_name}[{color_var}], {percentile} ), REMOVEFILTERS({dataset_name}[{location_var}]){filtering_dax} )\n')

            ''' Notes taken from original DAX

            /* Step 2: Calculate Bin Boundaries
            The Lower Bound of Bin 1 is the minimum value in the set, or the 0th percentile
            */

            /* Sometimes values are repeated throughout the set. For example, if you have many zero values.
            If the 20th percentile is the same as the 0th percentile, the upper bound is equal to the lower bound value, plus the lowest possible increment.
            So if the values being displayed are whole numbers, +1, if the precision is to the tens place (like the measure shown), increment by +0.1.
             Upper bound is the 20th percentile if it is not the same as the 0th percentile. */

             /* The lower bound of Bin 2 is the upper bound of bin 1, plus the lowest possible increment of the value being displayed.
            In this example, the value here goes out to the tens place.

            The upper bound of bin 2 has the same logic as the upper bound of bin 1 (check if the next percentile is the same as the previous),
             plus another logic check. It also checks If the lower bound of bin 2 is less than the 40th percentile.
                This check avoids the potential of the upper bound being lower than that of the lower bound of the same bin.
                 If either of these criteria are met, increment the lower bound by the most granular possible value based on the value being measured.

            This process repeats through bin 5.
            The lower bound of each bin is calculated in the same way, using the value of the upper bound of the previous bin.
            The upper bound is calculated based on the values of the percentiles calculated in step 1. */

            About the python code --------------------------------------------------------------------------
            This incredibly dense and complicated process recreates a bunch of power BI measures.
            The easiest way to inspect the measures is run this script and then open the TMDL file and look at the generated DAX

            I have no idea how leaflet, shiny or ggplot2 calculates percentile bins under the hood and/or on the fly
            And that's sort of the point, it amazes me that microsoft creates a supposedly "business user friendly" "low code" product
            That requires the user writing a bunch of complicated code to implement binning, when you can do it in R right out of the box
            with only a few lines of code.....

            '''
            for i in range(0, len(percentile_bin_breaks)):
                if i == 0:
                    file.write(f'\t\t\tVAR bin{i + 1}_LB = perc_{round(percentile_bin_breaks[i] * 100)}\n')
                    file.write(f'\t\t\tVAR bin{i + 1}_UB = IF ( perc_{round(percentile_bin_breaks[i] * 100)} == perc_{round(percentile_bin_breaks[i + 1] * 100)}, bin{i +1}_LB + 0.01, perc_{round(percentile_bin_breaks[i + 1] * 100)})\n')

                elif i < (len(percentile_bin_breaks) -1):
                    file.write(f'\t\t\tVAR bin{i + 1}_LB = bin{i}_UB + 0.01\n')
                    file.write(f'\t\t\tVAR bin{i + 1}_UB = IF ( perc_{round(percentile_bin_breaks[i] * 100)} == perc_{round(percentile_bin_breaks[i + 1] * 100)} || perc_{round(percentile_bin_breaks[i + 1] * 100)} <= bin{i+1}_LB, bin{i+1}_LB + 0.01, perc_{round(percentile_bin_breaks[i + 1] * 100)} )\n')

            file.write("\t\t\tRETURN\n\n")
            # pylint: enable=consider-using-enumerate

            '''From the original DAX

            /* Step 3: Assign bins to the counties in the map (output of the measure)
            For a given county, assign the appropriate bin number (1 through 5) depending on where that counties value falls relative to the bin boundaries
            calculated above. Here's I'm also adding a "zeroeth" bin, to capture counties that don't have data. If the measure of interest is blank, assign zero.
            */
            '''

            file.write("\t\t\t\tSWITCH (\n")
            file.write("\t\t\t\t\tTRUE (),\n")
            file.write("\t\t\t\t\tISBLANK([Measure Value]), 0,\n")

            for i in range(0, len(percentile_bin_breaks)):

                # make sure we have n -1 bins
                if i < (len(percentile_bin_breaks) -1):
                    file.write(f"\t\t\t\t\t[Measure Value] >= ROUND(bin{i+1}_LB,2) &&\n")

                    # Make sure the last line doesn't end with a comma
                    if i < (len(percentile_bin_breaks) -2):
                        file.write(f"\t\t\t\t\t[Measure Value] <= ROUND(bin{i+1}_UB,2), {i +1},\n")

                    else:
                        file.write(f"\t\t\t\t\t[Measure Value] <= ROUND(bin{i+1}_UB,2), {i +1}\n")


            file.write("\n\t\t\t\t)\n\t\t\t```\n")
            file.write("\t\tformatString: 0\n")
            file.write(f"\t\tlineageTag: {str(uuid.uuid4())}\n\n")
            '''


            '''
            # Generate bin ranges for each of the different bins we've been defining
            # see function definition above
            for i in range(1,len(percentile_bin_breaks)):
                self._generate_bin_ranges(           bin_number=i,
                                                     percentile_bin_breaks = percentile_bin_breaks,
                                                     dataset_file_path = dataset_file_path,
                                                     dataset_name = dataset_name,
                                                     color_var = color_var,
                                                     location_var = location_var,
                                                     filtering_dax = filtering_dax)

            # Create an empty bin measure
            file.write("\tmeasure 'Empty Bin' =\n\n")
            file.write('\t\t\t"No Data"\n')
            file.write(f"\t\tlineageTag: {str(uuid.uuid4())}\n\n")

            # Create measures for percentiles
            for i in range(1, len(percentile_bin_breaks)):
                file.write(f"\tmeasure '{round(percentile_bin_breaks[i] * 100)} percentile' = ```\n\n")
                file.write(f'\t\t\t\tCALCULATE ( PERCENTILE.INC ({dataset_name}[{color_var}], {percentile_bin_breaks[i]} ), REMOVEFILTERS({dataset_name}[{location_var}]){filtering_dax}  )\n\t\t\t```\n')
                file.write(f"\t\tlineageTag: {str(uuid.uuid4())}\n\n")
                file.write('\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}\n\n')
