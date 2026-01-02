'''A generic class for Power BI visuals. Used as a base class for all subtypes of visuals'''

import os

class _Visual:

    '''A generic class for Power BI visuals. Used as a base class for all subtypes of visuals'''

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=import-outside-toplevel

    def __init__(self,
                 page,
                 *,
                 visual_id,
                  height,
                  width,
                  x_position,
                  y_position,

                  visual_title=None,
                  visual_title_font_size=None,
                  z_position = 6000,
                  tab_order=-1001,
                  parent_group_id = None,
                  alt_text="A generic visual",
                  background_color=None,
                  background_color_alpha=None,
                  fill_color=None,
                  fill_color_alpha=None
                  ):

        #from powerbpy.page import _Page

        # checks ---------------------------------------------------------
        #if not isinstance(page, _Page):
        #    raise TypeError("Visuals must be added to a specific page")

        self.page = page
        self.dashboard = page.dashboard
        self.visual_id = visual_id
        self.visual_title = visual_title
        self.visual_title_font_size = visual_title_font_size
        self.height = height
        self.width = width
        self.x_position = x_position
        self.y_position = y_position
        self.z_position = z_position
        self.tab_order = tab_order
        self.parent_group_id = parent_group_id
        self.alt_text = alt_text
        self.background_color = background_color
        self.background_color_alpha = background_color_alpha
        self.fill_color = fill_color
        self.fill_color_alpha = fill_color_alpha

        # Define generic properties
        self.powerbi_schema = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/1.3.0/schema.json"
        self.visual_type = "GENERIC_VISUAL"



        # visual id unique?
        self.new_visual_folder = os.path.join(self.page.visuals_folder, self.visual_id)
        self.visual_json_path = os.path.join(self.new_visual_folder, "visual.json")

        if os.path.isdir(self.new_visual_folder) is True:
            raise ValueError('A visual with that visual_id already exists! Try using a different visual_id')

        os.makedirs(self.new_visual_folder)

        # variable type checks
        for var in [self.height, self.width, self.x_position, self.y_position, self.z_position, self.tab_order, self.background_color_alpha]:
            # Get the name of the variable from the locals()var_name = [name for name, value in locals().items() if value is var][0]

            if var is not None:
                if not isinstance(var, int):
                    raise ValueError(f"Sorry! The {var} variable must be an integer. Please confirm you didn't put quotes around a number")


        # Define the generic json for the visual
        self.visual_json = {
            "$schema": self.powerbi_schema,
            "name": self.visual_id,
            "position": {
                "x": self.x_position,
                "y": self.y_position,
                "z": self.z_position,
                "height": self.height,
                "width": self.width,
                "tabOrder": self.tab_order,
                },

            "visual": {
                "visualType": self.visual_type,
                "objects": {
                    "fill": [
                        {
                            "properties": {
                            "show": {
                                "expr": {
                                    "Literal": {
                                        "Value": "false"
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
                                          ]},

                "visualContainerObjects": {
                    "general": [
                        {
                            "properties": {
                                "altText": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{self.alt_text}'"
                                            }
                                        }
                                    }}
                                    }
                                ],
                    "title": [],
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
                    }                                          },
                "drillFilterOtherVisuals": True

                }

        # Add a title to the visual if the user provides one
        if self.visual_title is not None:
            self.visual_json["visual"]["visualContainerObjects"]["title"].append(

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
                                    "Value": f"'{self.visual_title}'"
                                }
                            }
                        }


                    }

                }

            )

            if self.visual_title_font_size is not None:
                self.visual_json["visual"]["visualContainerObjects"]["title"][0]["properties"]["fontSize"] = {
                            "expr": {
                                "Literal": {
                                    "Value": f"{self.visual_title_font_size}D"
                                }
                            }
                        }

        # add a background color if the user provided one
        if self.background_color is not None:
            self.visual_json["visual"]["visualContainerObjects"]["background"].append( {
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

            self.visual_json["visual"]["visualContainerObjects"]["background"].append( {
                    "properties": {
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{self.background_color}'"
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

        if self.background_color_alpha is not None:
            for bg_obj in self.visual_json["visual"]["visualContainerObjects"]["background"]:
                if "transparency" in bg_obj.get("properties", {}):
                    bg_obj["properties"]["transparency"]["expr"]["Literal"]["Value"] = f"{background_color_alpha}D"


        # add a fill color if the user provided one
        if self.fill_color is not None:
            self.visual_json["visual"]["objects"]["fill"].append( {
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

            self.visual_json["visual"]["objects"]["fill"].append(         {
                "properties": {
                    "fillColor": {
              "solid": {
                "color": {
                  "expr": {
                     "Literal": {
                                            "Value": f"'{self.fill_color}'"
                                        }
                  }
                }
              }
            }
          },
          "selector": {
            "id": "default"
          }


        })

        if self.fill_color_alpha is not None:
            for bg_obj in self.visual_json["visual"]["objects"]["fill"]:
                if "transparency" in bg_obj.get("properties", {}):
                    bg_obj["properties"]["transparency"]["expr"]["Literal"]["Value"] = f"{fill_color_alpha}D"

        # add the parent group id if the user supplies one
        if self.parent_group_id is not None:
            self.visual_json["parentGroupName"] = self.parent_group_id
