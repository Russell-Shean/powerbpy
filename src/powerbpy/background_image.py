import os
import uuid
import shutil
import json

from pathlib import Path
from importlib import resources

from powerbpy.page import Page

class BackgroundImage:

	def __init__(self,
				 page,
				 img_path,
				 alpha = 51,
				 scaling_method = "Fit"):

		self.page = page
		self.dashboard = page.dashboard



		if type(alpha) is not int:
			raise TypeError("alpha (the transparency value) must be an integer between 1-100")

		if (alpha > 100) or (alpha < 0):
			raise ValueError("alpha (the transparency value) must be an integer between 1-100")

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
		for dict in report_json["resourcePackages"]:
			if dict["name"] == "RegisteredResources":
				dict["items"].append(
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