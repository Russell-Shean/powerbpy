""" A subset of the Visual class. This represents text boxes"""

import json

from powerbpy.visual import _Visual


class _TextBox(_Visual):
    """ A subset of the Visual class. This represents text boxes"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=duplicate-code

    def __init__(self,
                 page,
                 *,
                 text,
                 visual_id,
                 height,
                 width,
                 x_position,
                 y_position,
                 z_position=6000,
                 tab_order=-1001,
                 parent_group_id=None,
                 alt_text="A text box",
                 text_align = "left",
                 font_weight = "bold",
                 font_size=32,
                 font_color="#000000",
                 background_color = None,
                 background_color_alpha=None
                 ):

        '''Add a text box to a page

        Parameters
        ----------
        text: str
            The text you want to display in the box
        visual_id: str
            Please choose a unique id to use to identify the text box. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        height:int
            Height of text box on the page
        width: int
            Width of text box on the page
        x_position: int
            The x coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        text_align: str
            How would you like the text aligned (available options: "left", "right", "center")
        font_weight: str
            This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
        font_size: int
            The font size in pts. Must be a whole integer. Defaults to 32 pt
        font_color: str
            Hex code for the font color you'd like to use. Defaults to black (#000000)
        background_color: str
            Hex code for the background color of the text box. Defaults to None (transparent)
        parent_group_id: str
            This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group.

        Notes
        -----
        This function creates a new text box on a page.
        '''

        super().__init__(page=page,
                  visual_id=visual_id,

                  height=height,
                  width=width,
                  x_position=x_position,
                  y_position=y_position,

                  z_position=z_position,
                  tab_order=tab_order,
                  parent_group_id=parent_group_id,
                  alt_text=alt_text,
             background_color=background_color,
             background_color_alpha=background_color_alpha,
)

        # checks --------------------------------------------------------------------------------------------------------------


        # Update the visual type
        self.visual_json["visual"]["visualType"] = "textbox"

        ## objects
        self.visual_json["visual"]["objects"]["general"] = [
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



        # add a background color if the user provided one
        if background_color is not None:
            self.visual_json["visual"]["visualContainerObjects"]["background"] =  [
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
                }

            ]

        else:
            self.visual_json["visual"]["visualContainerObjects"]["background"] = [
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



        # Write out the new json
        with open(self.visual_json_path, "w", encoding="utf-8") as file:
            json.dump(self.visual_json, file, indent = 2)
