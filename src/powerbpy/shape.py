"""A class representing shapes added dashboards"""

import json

from powerbpy.visual import _Visual

class _Shape(_Visual):
    """This class is for shapes such as arrows that you can add to a page"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=duplicate-code

    def __init__(self,
                 page,
                 *,
                         visual_id,
                         shape_type, 
                            x_position,
                            y_position,
                            height,
                            width,
                            parent_group_id,
                            fill_color,
                            fill_color_alpha,
                           #background_color,
                            #background_color_alpha,
                            tab_order,
                            z_position,
                            shape_rotation_angle=0,
                            alt_text="A shape"):

        '''This function adds a new shape to a page in a power BI dashboard report.

        Parameters
        ----------
        shape_type : str      
            The type of shape you want to put on the page. For example an arrow would be "arrow"
        shape_rotation_angle : str
            The angle that you want to rotate the shape by. Defaults to 0, or no rotation.
        alt_text : str
            Alternate text for the visualization can be provided as an argument. This is important for screen readers (accesibility) or if the visualization doesn't load properly.
        chart_title_font_size: int
            Font size for chart title
        x_position : int
            The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        y_position : int
            The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        height : int
            Height of chart on the page
        width : int
            Width of chart on the page
        tab_order : int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position : int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

        '''

        self.page = page
        self.x_position = x_position

        super().__init__(page=page,
                  visual_id=visual_id,
                  height=height,
                  width=width,
                  x_position=self.x_position,
                  y_position=y_position,
                  fill_color=fill_color,
                  fill_color_alpha=fill_color_alpha,

                  z_position=z_position,
                  tab_order=tab_order,
                  parent_group_id=parent_group_id,
                  alt_text=alt_text,
               #   background_color=background_color,
                #  background_color_alpha=background_color_alpha
                )


        # Create the json that defines the visual --------------------------------------------------------------
        # Update the visual type
        self.visual_json["visual"]["visualType"] = "shape"

        ## objects
        self.visual_json["visual"]["objects"]["shape"] = [
             { "properties": {
            "tileShape": {
                 "expr": {
                    "Literal": {
                        "Value": f"'{shape_type}'"
                        }
              }
            }
          }
        }
        ]


        # Set the rotation angle
        self.visual_json["visual"]["objects"]["rotation"] = [
               {
              "properties": {
                "shapeAngle": {
                    "expr": {
                        "Literal": {
                            "Value": f"{shape_rotation_angle}L"
                            }
                            }
                            }}


        }

        ]

        # Write out the new json
        with open(self.visual_json_path, "w", encoding="utf-8") as file:
            json.dump(self.visual_json, file, indent = 2)
