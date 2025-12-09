"""A class representing sanky chart visuals"""

import json

class _SankyChart(_Visual):
    """A class representing sanky chart visuals"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=duplicate-code

    def __init__(self,
                 page,
                 *,
                         visual_id,
                            data_source,
                            starting_var,
                            starting_var_values,
                            ending_var,
                            ending_var_values,
                            values_from_var,
                            x_position,
                            y_position,
                            height,
                            width,
                            chart_title,
                            link_colors,
                            parent_group_id,
                            background_color,
                            background_color_alpha,
                            chart_title_font_size,
                            #label_font_size,
                            tab_order,
                            z_position,
                            alt_text="A sankey chart"):

        '''This function adds a new chart to a page in a power BI dashboard report.

        Parameters
        ----------
        chart_id: str
            Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        chart_type: str
            The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
        data_source: str
            The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        starting_var: str
            Which variable from the data_source, do you want to use for the left side of the sanky chart?
        starting_var_values: list
            Which individual values do you want to use for the left side of the sanky chart? In general, this will probably mean all the unique values in the starting_var column. This function is setup to assume that you already know the structure of your data and can pass a list of unique values.
        ending_var: str
            Which variable from the data_source, do you want to use for the right side of the sanky chart?
        ending_var_values: list
            Which individual values do you want to use for the right side of the sanky chart? In general, this will probably mean all the unique values in the starting_var column. This function is setup to assume that you already know the structure of your data and can pass a list of unique values.
        values_from_var: str
            This is the variable that you want to count unique instances of as grouped by starting and ending variables. For now it only counts unique variables, but I'd like to add the option to provide a sum too
        chart_title: str
            Give your chart an informative title!:D
        alt_text: str
            Alternate text for the visualization can be provided as an argument. This is important for screen readers (accesibility) or if the visualization doesn't load properly.
        chart_title_font_size: int
            Font size for chart title
        label_font_size: int
            Font size for the labels on the various sanky nodes
        link_colors: list
            Here you can provide a list of Hex code colors for the connections between the different categories in the Sanky chart. In general this should be equal to the length of starting_var_values multiplied by the length of ending_var_values. If an argument is not provided the function assigns default colors.
        x_axis_var: str
            Column name of a column from data_source that you want to use for the x axis of the chart
        y_axis_var: str
            Column name of a column from data_source that you want to use for the y axis of the chart
        y_axis_var_aggregation_type: str
            Type of aggregation method you want to use to summarize y axis variable. Available options include" ["Sum", "Count", "Average"]
        x_position: int
            The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        height: int
            Height of chart on the page
        width: int
            Width of chart on the page
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

        '''
        from powerbpy.visual import _Visual

        self.page = page
        self.x_position = x_position

        super().__init__(page=page,
                  visual_id=visual_id,
                  visual_title=chart_title,
                  visual_title_font_size=chart_title_font_size,

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


        # Create the json that defines the visual --------------------------------------------------------------
        # Update the visual type
        self.visual_json["visual"]["visualType"] = "sankey02300D1BE6F5427989F3DE31CCA9E0F32020"
        self.visual_json["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json"

        ## query -----
        self.visual_json["visual"]["query"] = {
            "queryState": {
                "Source": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Entity": data_source
                                        }
                                    },
                                    "Property": starting_var
                                }
                            },
                            "queryRef": f"{data_source}.{starting_var}",
                            "nativeQueryRef": starting_var
                        }
                    ]
                },
                "Destination": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Entity": data_source
                                        }
                                    },
                                    "Property": ending_var
                                }
                            },
                            "queryRef": f"{data_source}.{ending_var}",
                            "nativeQueryRef": ending_var
                        }
                    ]
                },
                "Weight": {
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
                                            "Property": values_from_var
                                        }
                                    },
                                    "Function": 5
                                }
                            },
                            "queryRef": f"CountNonNull({data_source}.{values_from_var})",
                            "nativeQueryRef": f"Count of {values_from_var}"
                        }
                    ]
                }
            }
        }


        ## objects
        self.visual_json["visual"]["objects"]["linkLabels"] = [
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

        self.visual_json["visual"]["objects"]["links"] = []

        self.visual_json["visual"]["objects"]["cyclesLinks"] =  [
                {
                    "properties": {
                        "drawCycles": {
                            "expr": {
                                "Literal": {
                                    "Value": "0D"
                                }
                            }
                        },
                        "selfLinksWeight": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        }
                    }
                }
            ]

        self.visual_json["visual"]["objects"]["scaleSettings"] = [
                {
                    "properties": {
                        "provideMinHeight": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "lnScale": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        }
                    }
                }
            ]

        self.visual_json["visual"]["objects"]["cyclesLinks"] = [
                {
                    "properties": {
                        "nodesWidth": {
                            "expr": {
                                "Literal": {
                                    "Value": "10D"
                                }
                            }
                        }
                    }
                }
            ]


        # Create the links between the user provided values
        # It may be possible with Power BI to specify complicated charts (ie not all the possible nodes link together)
        # But for now we're just going to link all the provided nodes together
        for left_var_value in starting_var_values:
            for right_var_value in ending_var_values:
                # append to the links list
                self.visual_json["visual"]["objects"]["links"].append(

                 {

                    "properties": {
                        "fill": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "ThemeDataColor": {
                                            "ColorId": 4,
                                            "Percent": 0
                                        }
                                    }
                                }
                            }
                        }
                    },

                    "selector": {
                        "data": [
                            {
                                "scopeId": {
                                    "Comparison": {
                                        "ComparisonKind": 0,
                                        "Left": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Entity": data_source
                                                    }
                                                },
                                                "Property": starting_var
                                            }
                                        },
                                        "Right": {
                                            "Literal": {
                                                "Value": f"'{left_var_value}'"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "scopeId": {
                                    "Comparison": {
                                        "ComparisonKind": 0,
                                        "Left": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Entity": data_source
                                                    }
                                                },
                                                "Property": ending_var
                                            }
                                        },
                                        "Right": {
                                            "Literal": {
                                                "Value": f"'{right_var_value}'"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            )

        if link_colors:
            # Check to make sure that the number of colors match the number of links
            if len(link_colors) != len(self.visual_json["visual"]["objects"]["links"]):
                raise ValueError('If provided the number of link colors must be equal to the number of links')

            for i, color in enumerate(link_colors):
                self.visual_json["visual"]["objects"]["links"][i]["properties"]["fill"]["solid"]["color"] = {
                    "expr": {
                        "Literal": {
                            "Value": f"'{color}'"
                            }
                        }
                    }


        else:
            # Provide some random default colors
            default_link_colors = []

            for i in range(len(ending_var_values)):
                default_link_colors.extend([i+2] * len(starting_var_values))


            for i, color in enumerate(default_link_colors):
                self.visual_json["visual"]["objects"]["links"][i]["properties"]["fill"]["solid"]["color"] =  {

                                    "expr": {
                                        "ThemeDataColor": {
                                            "ColorId": color,
                                            "Percent": 0.4
                                        }

                                }
            }

        # Write out the new json
        with open(self.visual_json_path, "w", encoding="utf-8") as file:
            json.dump(self.visual_json, file, indent = 2)
