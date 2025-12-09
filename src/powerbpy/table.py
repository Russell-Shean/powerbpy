"""A class representing table visuals"""

import json

from powerbpy.visual import _Visual

class _Table(_Visual):
    """A class representing table visuals"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=duplicate-code

    def __init__(self,
                 page,
                 *,
                       visual_id,
                            data_source,
                            variables,
                            x_position,
                            y_position,
                            height,
                            width,
                            add_totals_row = False,
                            table_title = None,
                            table_title_font_size=None,
                            column_widths = None,
                            tab_order = -1001,
                            z_position = 6000,
                            alt_text="A table",
                            parent_group_id=None,
                            background_color="#FFFFFF",
                            background_color_alpha=None):

        '''This function adds a new table to a page in a power BI dashboard report.
        Parameters
        ----------

        visual_id: str
            Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        data_source: str
            The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        variables: list
            The variables from the table that you want to include
        table_title: str
            Give your table an informative title!:D
        column_widths: dict
            Optional. Provide the width of columns. Provide the widths as a dictionary with column names as keys and widths as values.
        x_position: int
            The x coordinate of where you want to put the table on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the table on the page. Origin is page's top left corner.
        height: int
            Height of table on the page
        width: int
            Width of table on the page
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

        '''

        self.page = page
        self.x_position = x_position

        super().__init__(page=page,
                  visual_id=visual_id,
                  visual_title=table_title,
                  visual_title_font_size=table_title_font_size,
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

        # define the json for the new chart

        # Create the json that defines the visual --------------------------------------------------------------
        # Update the visual type
        self.visual_json["visual"]["visualType"] =  "tableEx"
        self.visual_json["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json"

        ## query -----
        self.visual_json["visual"]["query"] = {
            "queryState": {
                "Values": {
                    "projections": []
                }
            }
        }

        # Objects
        self.visual_json["visual"]["objects"]["columnWidth"] = []

        self.visual_json["visual"]["objects"]["total"] = [
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

        # loop through the variables and add them to the json
        for variable in variables:

            # Add to the visual bit
            self.visual_json["visual"]["query"]["queryState"]["Values"]["projections"].append(


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
                for col_width_entry in self.visual_json.get("visual", {}) \
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
            for total_entry in self.visual_json.get("visual", {}) \
                                                                 .get("objects", {}) \
                                                                 .get("total", []):

                total_entry["properties"]["totals"]["expr"]["Literal"]["Value"] = "true"


        # Write out the new json
        with open(self.visual_json_path, "w", encoding="utf-8") as file:
            json.dump(self.visual_json, file, indent = 2)
