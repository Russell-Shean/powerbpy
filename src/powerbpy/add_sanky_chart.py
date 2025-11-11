import os, json



def add_sanky_chart(dashboard_path,
              page_id, 
              chart_id, 
              data_source, 
              starting_var, 
              ending_var,
              weight_var, 
              x_position, 
              y_position, 
              height, 
              width,
              chart_title,
              chart_title_font_size = 17,
              tab_order = -1001,
              z_position = 6000 ):

  '''This function adds a new chart to a page in a power BI dashboard report. 

  :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
  :param str page_id: The unique id for the page you want to add the background image to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
  :param str chart_id: Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
  
  :param str chart_type: The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
  :param str data_source: The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard. 
  
  :param str chart_title: Give your chart an informative title!:D
  :param int chart_title_font_size: Font Size for chart title

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




  sanky_json = {
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
  "name": "eb01a350900582cb1005",
  "position": {
    "x": x_position,
    "y": y_position,
    "z": z_position,
    "height": height,
    "width": width,
    "tabOrder": tab_order
  },
  "visual": {
    "visualType": "sankey02300D1BE6F5427989F3DE31CCA9E0F32020",
    "query": {
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
                      "Property": weight_var
                    }
                  },
                  "Function": 5
                }
              },
              "queryRef": f"CountNonNull({data_source}.{weight_var})",
              "nativeQueryRef": f"Count of {weight_var}"
            }
          ]
        }
      }
    },
    "objects": {
      "nodeComplexSettings": [
        {
          "properties": {
            "nodePositions": {
              "expr": {
                "Literal": {
                  "Value": "'[{\"name\":\"Large_SK_SELFLINK\",\"x\":\"0\",\"y\":\"0\"},{\"name\":\"Medium_SK_SELFLINK\",\"x\":\"0\",\"y\":\"261\"},{\"name\":\"Small_SK_SELFLINK\",\"x\":\"0\",\"y\":\"530\"},{\"name\":\"Large\",\"x\":\"570\",\"y\":\"0\"},{\"name\":\"Medium\",\"x\":\"570\",\"y\":\"179\"},{\"name\":\"Small\",\"x\":\"570\",\"y\":\"359\"}]'"
                }
              }
            },
            "viewportSize": {
              "expr": {
                "Literal": {
                  "Value": "'{\"height\":\"622.7999992370605\",\"width\":\"591\"}'"
                }
              }
            }
          }
        }
      ],
      "linkLabels": [
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
      "links": [
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
                        "Value": "'Large'"
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
                        "Value": "'Large'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 5,
                      "Percent": 0.4
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
                        "Value": "'Large'"
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
                        "Value": "'Medium'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 2,
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
                        "Value": "'Large'"
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
                        "Value": "'Small'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
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
                        "Value": "'Medium'"
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
                        "Value": "'Large'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 5,
                      "Percent": 0.4
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
                        "Value": "'Medium'"
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
                        "Value": "'Medium'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 2,
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
                        "Value": "'Medium'"
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
                        "Value": "'Small'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 2,
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
                        "Value": "'Small'"
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
                        "Value": "'Small'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
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
                        "Value": "'Small'"
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
                        "Value": "'Large'"
                      }
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "properties": {
            "fill": {
              "solid": {
                "color": {
                  "expr": {
                    "ThemeDataColor": {
                      "ColorId": 5,
                      "Percent": 0.4
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
                        "Value": "'Small'"
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
                        "Value": "'Medium'"
                      }
                    }
                  }
                }
              }
            ]
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": "20D"
                }
              }
            },
            "forceDisplay": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            },
            "unit": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "cyclesLinks": [
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
      ],
      "scaleSettings": [
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
      ],
      "nodes": [
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
    },
    "visualContainerObjects": {
      "general": [
        {
          "properties": {
            "altText": {
              "expr": {
                "Literal": {
                  "Value": "'A sankey chart showing the change in starting size of a store to ending size. It is broken into Small, medium, and large.'"
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

  # If a chart title is provided, add it
  if chart_title:
    sanky_json["visual"]["visualContainerObjects"]["title"] = [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": f"'{chart_title}'"
                }
              }
            },
            "fontSize": {
              "expr": {
                "Literal": {
                  "Value": f"{chart_title_font_size}D"
                }
              }
            },
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
  ]
      


  
