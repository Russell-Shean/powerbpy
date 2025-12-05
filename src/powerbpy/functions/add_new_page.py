import os, json

import powerbpy as PBI


def add_new_page(dashboard_path, 
				 page_name, 
				 title = None, 
				 subtitle = None, 
				 displayOption = 'FitToPage'):

	'''Create a new blank dashboard page
	
	Parameters
	----------
	dashboard_path: str
	  The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
	page_name: str
	  The display name for the page you just created. This is different from the page_id which is only used internally. 
	title: str
	  Title to put at the top of the page. This under the hood calls the add_text_box() function. If you would like more control over the title's appearance use that function instead.
	subtitle: str
	  Subtitle to put at the top of the page. This under the hood calls the add_text_box() function. If you would like more control over the title's appearance use that function instead.
	displayOption: str
	  Default way to display the page for end users (View -> Page View options in Power BI). Possible options: FitToPage, FitToWidth, ActualSize

	Returns
	-------
	new_page_id: str
	  The unique id for the page you just created. If you used this function it will be in the format page1, page2, page3, page4, etc. If you manually create a page it will be a randomly generated UUID. To find a page's page id, consult the report > definition> pages > page.json file and look in the page order list. 
	
	Notes
	----     
	In order to reference the page to add visuals to it later, you'll need to remember what order you created the pages in. The first page that is created when you first call `create_new_dashboard()` is called "page1", the next page you create is called "page2", the page after that is called "page3" etc. (I'm going to convert the functions to classes and methods soon at which point this paragraph will become irrelevant).        
	
	In our example, I'll create a new page called "Bee Colonies" and then we'll add a title called "The bees are in trouble!" and a subtitle below it called "We're losing bee colonies". The title and subtitle arguments make a best guess about the best font and position for the text boxes that make up the title and subtitle. These arguments are optional, so if you don't want a title or subtitle, just leave the argument blank. If you want the title to have a different font, style, position, etc from the default use the `add_text_box()` function.      
	Here's the code to create a new (mostly blank) page:     
	
	```python
	PBI.add_new_page(dashboard_path = "C:/Users/Russ/PBI_projects/test_dashboard", 
					   page_name = "Bee Colonies",
					   title= "The bees are in trouble!",
					   subtitle = "We're losing bee colonies")
					   
	```
	Here's what the new page looks like in Power BI Desktop       
	![New Page Example](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/new_page_example.png?raw=true "Example Page")
	
	'''

	# file paths
	# Convert dashboard path to an absolute path if a relative path was provided
	dashboard_path = os.path.abspath(os.path.expanduser(dashboard_path))
	
	report_name = os.path.basename(dashboard_path)
	pages_folder = os.path.join(dashboard_path, f'{report_name}.Report/definition/pages' )
	pages_json_path = os.path.join(pages_folder, "pages.json")

	# determine number of pages
	with open(pages_json_path,'r') as file:
		pages_list = json.load(file)

		# determine number of pages
		n_pages = len(pages_list["pageOrder"])

		# create a new page id based on existing number of pages
		new_page_id = f"page{n_pages + 1}"

		# add the new page id to the pageOrder list
		pages_list["pageOrder"].append(new_page_id)
	
  
	# write to file
	with open(pages_json_path,'w') as file:
		json.dump(pages_list, file, indent = 2)

	
	# create a folder for the new page
	new_page_folder = os.path.join(pages_folder, new_page_id)
	new_page_json_path = os.path.join(new_page_folder, "page.json")
	os.makedirs(new_page_folder)

	# create a new json file for the new page
	new_page_json = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.2.0/schema.json",
					  "name": new_page_id,
					  "displayName": page_name,
					  "displayOption": displayOption,
					  "height": 720,
					  "width": 1280,
					  "objects":{}}


	# write to file
	with open(new_page_json_path, "w") as file:
		json.dump(new_page_json, file, indent = 2)


	# Add title and subtitle if requested 
	if title is not None:
		PBI.add_text_box(text = title,
			 dashboard_path= dashboard_path,
			   page_id= new_page_id,
				 text_box_id= f"{new_page_id}_title", 
				 height=68,
				   width=545,
					 x_position = 394, 
					 y_position = 44)

	if subtitle is not None:
		PBI.add_text_box(text = subtitle,
			 dashboard_path= dashboard_path,
			   page_id= new_page_id,
				 text_box_id= f"{new_page_id}_subtitle", 
				 height=38,
				   width=300,
					 x_position = 500, 
					 y_position = 93,
					 font_size = 14)



	return new_page_id
