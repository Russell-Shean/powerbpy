import os, uuid, shutil, json

from pathlib import Path
from importlib import resources

#import powerbpy

from powerbpy.dashboard import Dashboard

class Page:
	def __init__(self,
				 dashboard,
				 page_name, 
				 title = None, 
				 subtitle = None, 
				 displayOption = 'FitToPage'):

		if not isinstance(dashboard, Dashboard):
			raise TypeError("Pages must be attached to a Dashboard instance")

		# Get everything else from the dashboard
		# Attribute delegation (inherit parent instance attributes)
		def __getattr__(self, name):
			return getattr(self._dashboard, name)

		self.dashboard = dashboard
		self.page_name = page_name
		self.title = title
		self.subtitle = subtitle
		self.displayOption = displayOption
		
		# determine number of pages
		with open(self.dashboard.pages_file_path,'r') as file:
			pages_list = json.load(file)

		# determine number of pages
		n_pages = len(pages_list["pageOrder"])

		# create a new page id based on existing number of pages
		self.page_id = f"page{n_pages + 1}"

		# add the new page id to the pageOrder list
		pages_list["pageOrder"].append(self.page_id)
		
		# write to file
		with open(self.dashboard.pages_file_path,'w') as file:
			json.dump(pages_list, file, indent = 2)
			
		# create a folder for the new page
		self.page_folder = os.path.join(self.dashboard.pages_folder, self.page_id)
		self.page_json_path = os.path.join(self.page_folder, "page.json")
		os.makedirs(self.page_folder)
		
		# create a new json file for the new page
		page_json = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.2.0/schema.json",
					  "name": self.page_id,
					  "displayName": self.page_name,
					  "displayOption": self.displayOption,
					  "height": 720,
					  "width": 1280,
					  "objects":{}}
					  
		# write to file
		with open(self.page_json_path, "w") as file:
			json.dump(page_json, file, indent = 2)
			
			
		# Add title and subtitle if requested 
		if self.title is not None:
			PBI.add_text_box(text = self.title,
			 dashboard_path= dashboard_path,
			   page_id= self.page_id,
				 text_box_id= f"{self.page_id}_title", 
				 height=68,
				   width=545,
					 x_position = 394, 
					 y_position = 44)
					 
					 
		if subtitle is not None:
			PBI.add_text_box(text = self.subtitle,
			 dashboard_path= dashboard_path,
			   page_id= self.page_id,
				 text_box_id= f"{self.page_id}_subtitle", 
				 height=38,
				   width=300,
					 x_position = 500, 
					 y_position = 93,
					 font_size = 14)

		
