'''This class is used to represent background images that can be added to pages.
    You should never call this class directly, instead use the add_background_image() method attached to the Page class.
    See add_background_image() for more details.
'''

import os
import shutil
import json

class _BackgroundImage:

    '''This class is used to represent background images that can be added to pages.
    You should never call this class directly, instead use the add_background_image() method attached to the Page class.
    See add_background_image() for more details.
    '''

    def __init__(self,
                 page,
                 img_path,
                 alpha = 51,
                 scaling_method = "Fit"):

        '''Add a background image to a dashboard page
        Parameters
        ----------
        img_path: str
            The path to the image you want to add. (Can be a relative path because the image is copied to the report folder). Allowed image types are whatever PBI allows manually, so probably at least jpeg and png
        alpha: int
            The transparency of the background image. Must be a whole integer between 1 and 100.
        scaling_method: str
            The method used to scale the image available options include ["Fit", ]

        Notes
        ----
        Here's how you can add a background image to a page. To add the image, you'll need to provide the following required arguments:
            1. `img_path` - This is the path (relative or full) to the image you want to add to the dashboard

        There are two additional optional arguments:
            2. `alpha` - This is the image's transparency with 0 is fully transparent and 100 is full non-transparent (defaults to 100 )
            3. `scaling_method` - This tells Power BI how to scale the image (defaults to "Fit" which fits the image to the page)

        Here's some example code that adds a new background image to the Bee Colonies page:

        ```python
            page1.add_background_image(img_path = "examples/data/Taipei_skyline_at_sunset_20150607.jpg",
                   alpha = 51,
                   scaling_method = "Fit")
        ```
        And here's what the dashboard looks like, now that we've added a background image:
        ![Background Image Example](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/background_image_example.png?raw=true "Background Image Example")
        '''

        self.page = page
        self.dashboard = page.dashboard


        if not isinstance(alpha, int) or not (1 <= alpha <= 100):
            raise ValueError("alpha must be an integer between 1–100")

        # file paths
        # Convert dashboard path to an absolute path if a relative path was provided
        img_name = os.path.basename(img_path)

        # This is the location of the image within the dashboard
        registered_img_path = os.path.join(self.dashboard.registered_resources_folder, img_name)



        # Upload image to dashboard's registered resources ---------------------------------------------------

        # create registered resources folder if it doesn't exist
        if not os.path.exists(self.dashboard.registered_resources_folder):
            os.makedirs(self.dashboard.registered_resources_folder)

        # move image to registered resources folder
        shutil.copy(img_path, registered_img_path)

        # add new registered resource (the image) to report.json ----------------------------------------------
        with open(self.dashboard.report_json_path,'r', encoding="utf-8") as file:
            report_json = json.load(file)

        # add the image as an item to the registered resources items list
        for pack in report_json["resourcePackages"]:
            if pack["name"] == "RegisteredResources":
                pack["items"].append(
                                  {
                                    "name": img_name,
                                    "path": img_name,
                                    "type": "Image"
                                   }
                                )

        # write to file
        with open(self.dashboard.report_json_path,'w', encoding="utf-8") as file:
            json.dump(report_json, file, indent = 2)

        # Add image to page -------------------------------------------------------------------------------
        with open(self.page.page_json_path,'r', encoding="utf-8") as file:
            page_json = json.load(file)

        # add the image to the page's json
        page_json["objects"]["background"] = [
            {
                "properties": {
                    "image": {
                        "image": {
                            "name": {
                                "expr": {
                                    "Literal": {
                                        "Value": f"'{img_name}'"
                                        }
                                        }
                                    },

                            "url": {
                                "expr": {
                                    "ResourcePackageItem": {
                                        "PackageName": "RegisteredResources",
                                        "PackageType": 1,
                                        "ItemName": img_name
                                        }
                                        }
                                    },

                                "scaling": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{scaling_method}'"
                                            }
                                            }
                                            }
                                    }
                                },

                                "transparency": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"{alpha}D"
              }
            }
          }
        }
      }
    ]

        # write to file
        with open(self.page.page_json_path,'w', encoding="utf-8") as file:
            json.dump(page_json, file, indent = 2)
