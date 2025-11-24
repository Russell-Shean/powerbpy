#background_image
import os, shutil, json

def add_background_image(dashboard_path, page_id, img_path, alpha = 100, scaling_method = "Fit"):

	'''Add a background image to a dashboard page
	
	Parameters
	----------
	dashboard_path: str
	  The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
	page_id: str
	  The unique id for the page you want to add the chart to. If you used this package's functions it will be in the format page1, page2, page3, page4, etc. If you manually created the page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
	img_path: str
	  The path to the image you want to add. (Can be a relative path because the image is copied to the report folder). Allowed image types are whatever PBI allows manually, so probably at least jpeg and png
	alpha: int
	  The transparency of the background image. Must be a whole integer between 1 and 100. 
	scaling_method: str
	  The method used to scale the image available options include ["Fit", ]
	  
	Notes
	----
	Here's how you can add a background image to a page. To add the image, you'll need to provide the following required arguments:     
  1. `dashboard_path` - This is the path (relative or full) to the dashboard's project folder       
  2. `page_id` - This is the identifier for the page you want to put the background image on. The first page that is created when you first call `create_new_dashboard()` is called "page1", the next page you create is called "page2", the page after that is called "page3" etc.        
  3. `img_path` - This is the path (relative or full) to the image you want to add to the dashboard       
  
  The first two arguments will be replaced by something like `myDashboard.page1.add_background_image()` when I convert the package to OOP.      
  
  There are two additional optional arguments:     
  4. `alpha` - This is the image's transparency with 0 is fully transparent and 100 is full non-transparent (defaults to 100 )    
  5. `scaling_method` - This tells Power BI how to scale the image (defaults to "Fit" which fits the image to the page)      
  Here's some example code that adds a new background image to the Bee Colonies page:     
  ```python
     PBI.add_background_image(dashboard_path = "C:/Users/Russ/PBI_projects/test_dashboard", 
	               page_id = "page2", 
	               img_path = "examples/data/Taipei_skyline_at_sunset_20150607.jpg", 
	               alpha = 51,
	               scaling_method = "Fit")
	```       
  
  And here's what the dashboard looks like, now that we've added a background image:      
  ![Background Image Example](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/background_image_example.png?raw=true "Background Image Example")   

	'''

	if type(alpha) is not int:
		raise TypeError("alpha (the transparency value) must be an integer between 1-100")

	if (alpha > 100) or (alpha < 0):
		raise ValueError("alpha (the transparency value) must be an integer between 1-100")

	# file paths
	# Convert dashboard path to an absolute path if a relative path was provided
	dashboard_path = os.path.abspath(os.path.expanduser(dashboard_path))
	
	report_name = os.path.basename(dashboard_path)
	img_name = os.path.basename(img_path)

	report_folder = os.path.join(dashboard_path, f'{report_name}.Report')
	definitions_folder = os.path.join(report_folder, "definition")

	page_json_path = os.path.join(definitions_folder, f"pages/{page_id}/page.json")
	report_json_path = os.path.join(definitions_folder, "report.json")


	registered_resources_folder = os.path.join(report_folder, "StaticResources/RegisteredResources")

	# This is the location of the image within the dashboard
	registered_img_path = os.path.join(registered_resources_folder, img_name)


	# Upload image to dashboard's registered resources ---------------------------------------------------

	# create registered resources folder if it doesn't exist
	if not os.path.exists(registered_resources_folder):
		os.makedirs(registered_resources_folder)

	# move image to registered resources folder
	shutil.copy(img_path, registered_img_path)


	# add new registered resource (the image) to report.json ----------------------------------------------
	with open(report_json_path,'r') as file:
		report_json = json.load(file)


	# add the image as an item to the registered resources items list
	for dict in report_json["resourcePackages"]:
		if dict["name"] == "RegisteredResources":
			dict["items"].append(
								  {
									"name": img_name,
									"path": img_name,
									"type": "Image"
								   }   
								)



	#print(report_json)

   
	# write to file
	with open(report_json_path,'w') as file:
		json.dump(report_json, file, indent = 2)




	# Add image to page -------------------------------------------------------------------------------
	with open(page_json_path,'r') as file:
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
	with open(page_json_path,'w') as file:
		json.dump(page_json, file, indent = 2)





