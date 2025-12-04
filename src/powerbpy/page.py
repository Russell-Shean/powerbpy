import os, uuid, shutil, json

from pathlib import Path
from importlib import resources

#import powerbpy

from powerbpy.dashboard import Dashboard

class Page:
	
	# Get everything else from the dashboard
	# Attribute delegation (inherit parent instance attributes)

	def __init__(self,
				 dashboard,
				 page_name, 
				 title = None, 
				 subtitle = None, 
				 displayOption = 'FitToPage'):

		if not isinstance(dashboard, Dashboard):
			raise TypeError("Pages must be attached to a Dashboard instance")


		# Define lists of objects that can be associated with a page
		self.background_images = []
		self.visuals = []

		

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

		# Add subfolders for visuals and stuff
		self.visuals_folder = os.path.join(self.page_folder, "visuals")

		
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
			self.add_text_box(text = self.title,
				            visual_id= f"{self.page_id}_title", 
				 height=68,
				   width=545,
					 x_position = 394, 
					 y_position = 44)
					 
					 
		if subtitle is not None:
			self.add_text_box(text = self.subtitle,
			                  visual_id= f"{self.page_id}_subtitle", 
				 height=38,
				   width=300,
					 x_position = 500, 
					 y_position = 93,
					 font_size = 14)


	def add_background_image(self,
							 img_path, 
							 alpha = 51, 
							 scaling_method = "Fit"):
						 
						 
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

		# Local import avoids circular import at module load
		from powerbpy.background_image import BackgroundImage
		
		background_image = BackgroundImage(self,
						 img_path, 
						 alpha, 
						 scaling_method)

		self.background_images.append(background_image)
		return background_image
	
	def add_chart(self,
	              visual_id,
	             chart_type,
                 data_source,
                 chart_title,
                 x_axis_title,
                 y_axis_title,
                 x_axis_var,
                 y_axis_var,
                 y_axis_var_aggregation_type,
                 x_position,
                 y_position,
                 height,
                 width,
                 tab_order = -1001,
                 z_position = 6000, 
			     parent_group_id = None,
				 alt_text="A chart"):

		from powerbpy.chart import Chart

		chart = Chart(self,
		              visual_id=visual_id,
	                  chart_type=chart_type,
                 data_source=data_source,
                 visual_title=chart_title,
                 x_axis_title=x_axis_title,
                 y_axis_title=y_axis_title,
                 x_axis_var=x_axis_var,
                 y_axis_var=y_axis_var,
                 y_axis_var_aggregation_type=y_axis_var_aggregation_type,
                 x_position=x_position,
                 y_position=y_position,
                 height=height,
                 width=width,
                 tab_order=tab_order,
                 z_position=z_position, 
			     parent_group_id=parent_group_id,
				 alt_text=alt_text)

		self.visuals.append(chart)
		return chart

	def add_text_box(self,
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
				 background_color_alpha=None):

		from powerbpy.text_box import TextBox

		text_box = TextBox(self,
                 text=text, 
				 visual_id=visual_id, 
				 height=height, 
				 width=width,
				 x_position=x_position, 
				 y_position=y_position, 
				 z_position=z_position, 
				 tab_order=tab_order,
                 parent_group_id=parent_group_id,
				 alt_text=alt_text,
				 text_align=text_align, 
				 font_weight=font_weight, 
				 font_size=font_size, 
				 font_color=font_color, 
				 background_color=background_color,
				 background_color_alpha=background_color_alpha)

		self.visuals.append(text_box)
		return text_box

	def add_button(self,
                 label, 
                 visual_id, 
                 height, 
                 width,
                 x_position, 
                 y_position, 
                 z_position = 6000, 
                 tab_order=-1001, 
                 fill_color="#3086C3", 
                 alpha=0, 
                 url_link = None, 
                 page_navigation_link = None,
				 alt_text="A button"):

		from powerbpy.button import Button

		button = Button(self,
                 label=label, 
                 visual_id=visual_id, 
                 height=height, 
                 width=width,
                 x_position=x_position, 
                 y_position=y_position, 
                 z_position =z_position, 
                 tab_order=tab_order, 
                 fill_color=fill_color, 
                 alpha=alpha, 
                 url_link = url_link, 
                 page_navigation_link = page_navigation_link,
				 alt_text=alt_text)

		self.visuals.append(button)
		return(button)

	def add_slicer(self,
	              data_source, 
               column_name,    
			   visual_id, 
			   height, 
			   width,
			   x_position, 
			   y_position, 
			   z_position = 6000, 
			   tab_order=-1001,
			   title = None,
			   text_align = "left", 
			   font_weight = "bold", 
			   font_size=32, 
			   font_color="#000000", 
			   background_color = None, 
			   parent_group_id = None,
			   alt_text= "A slicer"):

		from powerbpy.slicer import Slicer

		slicer = Slicer(self,
		        data_source=data_source, 
               column_name=column_name,  
			   visual_id=visual_id, 
			   height=height, 
			   width=width,
			   x_position=x_position, 
			   y_position=y_position, 
			   z_position=z_position, 
			   tab_order=tab_order,
			   visual_title=title,
			   text_align=text_align, 
			   font_weight=font_weight, 
			   font_size=font_size, 
			   font_color=font_color, 
			   background_color=background_color, 
			   parent_group_id=parent_group_id, 
               alt_text = "A slicer")





		self.visuals.append(slicer)
		return(slicer)

	def add_card(self,
	             data_source, 
             measure_name, 

			 visual_id, 
			 height, 
			 width,
			 x_position, 
			 y_position, 
			 z_position = 6000, 
			 tab_order=-1001,
			 card_title = None,
			 text_align = "left", 
			 font_weight = "bold", 
			 font_size=32, 
			 font_color="#000000", 
			 background_color = None, 
			 background_color_alpha = None,
			 parent_group_id = None,
			 alt_text="A card"):
			 
		from powerbpy.card import Card
		
		card = Card(self,
	             data_source=data_source, 
             measure_name=measure_name, 

			 visual_id=visual_id, 
			 height=height, 
			 width=width,
			 x_position=x_position, 
			 y_position=y_position, 
			 z_position = z_position, 
			 tab_order=tab_order,
			 visual_title = card_title,
			 text_align = text_align, 
			 font_weight = font_weight, 
			 font_size=font_size, 
			 font_color=font_color, 
			 background_color = background_color,
			 background_color_alpha=background_color_alpha, 
			 parent_group_id = parent_group_id,
			 alt_text=alt_text)

		self.visuals.append(card)
		return card

	def add_shape_map(self,
	               visual_id, 
				  data_source, 
				  shape_file_path,
				  map_title, 
				  location_var, 
				  color_var,
				  color_palette, 
				  height, 
				  width,
				  x_position, 
				  y_position, 
				  add_legend = True, 
				  static_bin_breaks = None, 
				  percentile_bin_breaks = None, 
				  filtering_var = None,
				  z_position = 6000, 
				  tab_order=-1001,
                  parent_group_id = None,
                 alt_text = "A shape map"):

		from powerbpy.shape_map import ShapeMap

		shape_map = ShapeMap(self,
	               visual_id=visual_id, 
				  data_source=data_source, 
				  shape_file_path=shape_file_path,
				  map_title=map_title, 
				  location_var=location_var, 
				  color_var=color_var,
				  color_palette=color_palette, 
				  height=height, 
				  width=width,
				  x_position=x_position, 
				  y_position=y_position, 
				  add_legend = add_legend, 
				  static_bin_breaks = static_bin_breaks, 
				  percentile_bin_breaks = percentile_bin_breaks, 
				  filtering_var = filtering_var,
				  z_position = z_position, 
				  tab_order=tab_order,
                  parent_group_id = parent_group_id,
                 alt_text = alt_text)

		self.visuals.append(shape_map)
		return shape_map


		

		
		







		
