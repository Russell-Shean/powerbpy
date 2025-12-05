import os, uuid, shutil, json

from pathlib import Path
from importlib import resources

#import powerbpy

#from powerbpy.page import Page

#from .page import *

class Dashboard:
	'''A python class used to model a power BI dashboard project

	'''

	def __init__(self,
			     parent_dir,
				 report_name):
		'''A python class used to model a power BI dashboard project
		Parameters
		----------
		parent_dir: str
			The path to the directory where you want to store the new dashboard.
		report_name: str
			Name of the report.
		
		Returns
		-------
		None
		
		Notes
		-----
		- This function creates a power BI report in the specified parent directory.
		- The dashboard can be opened and edited in Power BI desktop like normal, or be further modified progromatically using other functions in this package.
		- The function creates a folder with the name report_name inside parent_dir with all the dashboard's files.
		- The dashboard uses a .pbip/.pbir format with TMDL enabled.
		- To publish this type of dashboard you will need to either use git enabled workspaces OR convert to a .pbit template and then to a .pbix file before publishing
		- These annoyances are worth it because the .pbir + TMDL format is the only one that allows real version control and programatic manipulation of the report using these functions.
		- (.pbip uses mimified json by default and throws an error when it's given unpacked json).
		
		- This dashboard turns off time intelligence and relationship autodection off by default
		'''

		# Define pages as a list of instances of the page class
		self.pages = []

		self.datasets = []



		# The parent directory should be converted to a full path
		# Because Power BI gets weird with relative paths

		# attributes provided by the user
		self.parent_dir = os.path.abspath(os.path.expanduser(parent_dir))
		self.report_name = report_name
		
		# Attributes calculated from what the user provides
		# create a new logical id field
		# see this for explanation of what a UUID is: https://stackoverflow.com/a/534847
		self.report_logical_id = str(uuid.uuid4())
		self.sm_logical_id = str(uuid.uuid4())
		
		# define page name
		#self.page1_name = "page1"
		
		# Define file paths ------------------------------------------------------------------------------------
		# Outer level directory --------------------------------------------------------------------------------
		self.project_folder_path = os.path.join(self.parent_dir, self.report_name)
		
		self.pbip_file_path = os.path.join(self.project_folder_path, f'{self.report_name}.pbip')
		
		## Report folder -----------------------------------------------------------------
		self.report_folder_path = os.path.join(self.project_folder_path, f'{self.report_name}.Report')
		self.platform_file_path = os.path.join(self.report_folder_path,  ".platform")
		self.pbir_file_path = os.path.join(self.report_folder_path, 'definition.pbir')

		self.registered_resources_folder = os.path.join(self.report_folder_path, "StaticResources/RegisteredResources")
		
		
		
	
		
		### definition folder -------------------------------------------------------------------------------------
		self.report_definition_folder = os.path.join(self.report_folder_path, 'definition')

		self.report_json_path = os.path.join(self.report_definition_folder, "report.json")
		
		self.pages_folder = os.path.join(self.report_definition_folder, 'pages')
		self.pages_file_path = os.path.join(self.pages_folder, "pages.json")

		
		#self.page1_folder = os.path.join(self.pages_folder, self.page1_name)
		#self.page1_json_path = os.path.join(self.page1_folder, "page.json")
		
		## report_name.SemanticModel folder ----------------------------------------------------------------------------
		self.semantic_model_folder_path = os.path.join(self.project_folder_path, f'{self.report_name}.SemanticModel')
		self.sm_platform_file_path = os.path.join(self.semantic_model_folder_path, ".platform")

		self.sm_definition_folder = os.path.join(self.semantic_model_folder_path, "definition")

		self.model_path = os.path.join(self.sm_definition_folder, 'model.tmdl')
		self.temp_model_path = os.path.join(self.project_folder_path, 'model2.tmdl')

		self.diagram_layout_path = os.path.join(self.semantic_model_folder_path, 'diagramLayout.json')
		self.tables_folder = os.path.join(self.sm_definition_folder, 'tables')

		# Start creating a new dashboard not just defining file paths ----------------------------
		# check to make sure parent directory exists
		if not os.path.exists(self.parent_dir):
			raise ValueError("The parent directory doesn't exist! Please create it and try again!")
			
		# make sure a report folder doesn't already exist
		if os.path.exists(self.project_folder_path):
			raise ValueError("Sorry a report with that name already exists! Please use a different report name or parent directory and try again")
			
		# Transfer all the blank dashboard files from the package resources ---------------------------------------------------
		traversable = resources.files("powerbpy.dashboard_resources")
		
		with resources.as_file(traversable) as path:
			shutil.copytree(path, self.project_folder_path)
			
		# Change file names -----------------------------------------------------------------------------------------------------
		os.rename(os.path.join(self.project_folder_path, "blank_template.Report"), self.report_folder_path)
		os.rename(os.path.join(self.project_folder_path, "blank_template.SemanticModel"), os.path.join(self.project_folder_path, f'{self.report_name}.SemanticModel'))
		os.rename(os.path.join(self.project_folder_path, "blank_template.pbip"), self.pbip_file_path)
		
		#os.rename(
		#	os.path.join(self.project_folder_path, 
		#	f'{self.report_name}.Report/definition/pages/915e09e5204515bccac2'), 
		#	os.path.join(self. project_folder_path, 
		#	f'{self.report_name}.Report/definition/pages/{self.page1_name}'))

		# Delete the first page so that we can create a new page one with the new_page() method
		default_first_page = os.path.join(self.project_folder_path, 
		                                  f'{self.report_name}.Report/definition/pages/915e09e5204515bccac2')
		
		shutil.rmtree(default_first_page)
			
		# Modify files --------------------------------------------------------------------
		## top level -----------------------------------------------------------------------
		# .pbip file
		with open(self.pbip_file_path,'r') as file:
			pbip_file = json.load(file)
		
		# modify the report path
		pbip_file["artifacts"][0]["report"]["path"] = f'{self.report_name}.Report'
		
		# write to file
		with open(self.pbip_file_path,'w') as file:
			json.dump(pbip_file, file, indent = 2)
		
		
		## report folder -----------------------------------------------------------------
		# .platform file
		with open(self.platform_file_path,'r') as file:
			platform_file = json.load(file)
		
		# modify the display name
		platform_file["metadata"]["displayName"] = f'{self.report_name}'
		
		# update the unique UUID
		platform_file["config"]["logicalId"] = self.report_logical_id
		
		# write to file
		with open(self.platform_file_path,'w') as file:
			json.dump(platform_file, file, indent = 2)
		
		
		#.pbir file
		with open(self.pbir_file_path,'r') as file:
			pbir_file = json.load(file)
			
		# modify the display name
		pbir_file["datasetReference"]["byPath"]["path"] = f'../{self.report_name}.SemanticModel'
		
		# write to file
		with open(self.pbir_file_path,'w') as file:
			json.dump(pbir_file, file, indent = 2)
		
		### definition folder --------------------------------------------------------
		# pages.json
		with open(self.pages_file_path,'r') as file:
			pages_file = json.load(file)
		
		pages_file["pageOrder"] = []
		pages_file["activePageName"] = "page1"
		
		# write to file
		with open(self.pages_file_path,'w') as file:
			json.dump(pages_file, file, indent = 2)
		
		#### page 1 folder
		#with open(self.page1_json_path,'r') as file:
		#	page1_json = json.load(file)
		
		
		#page1_json["name"] = self.page1_name
		
		# write to file
		#with open(self.page1_json_path,'w') as file:
		#	json.dump(page1_json, file, indent = 2)
		
		## Semantic model folder ----------------------------------------------------------------
		# .platform file
		with open(self.platform_file_path,'r') as file:
			platform_file = json.load(file)
		
		# modify the display name
		platform_file["metadata"]["displayName"] = f'{self.report_name}'
		
		# update the unique UUID
		platform_file["config"]["logicalId"] = self.sm_logical_id
		
		# write to file
		with open(self.platform_file_path,'w') as file:
			json.dump(platform_file, file, indent = 2)

	def new_page(self,
				 page_name, 
				 title = None, 
				 subtitle = None, 
				 displayOption = 'FitToPage'):
		'''Create a new blank dashboard page
		
		Parameters
		----------
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
		# Local import avoids circular import at module load
		from powerbpy.page import Page
		
		page = Page(self,
				 page_name=page_name, 
				 title =title, 
				 subtitle = subtitle, 
				 displayOption = displayOption)

		self.pages.append(page)
		return page

	def add_tmdl(self,
				 data_path = None, 
				 add_default_datetable = True):
		
		from powerbpy.dataset_tmdl  import Tmdl

		tmdl = Tmdl(self,
		            data_path, 
				    add_default_datetable)

		self.datasets.append(tmdl)
		return tmdl

	def add_local_csv(self,
	                  data_path):

		from powerbpy.dataset_csv import LocalCsv

		dataset = LocalCsv(self,
		                   data_path)
		
		self.datasets.append(dataset)
		return dataset

	def add_blob_csv(self,
				 data_path,
				 account_url, 
				 blob_name, 
				 tenant_id = None, 
				 use_saved_storage_key = False,  
				 SAS_url = None,
				 storage_account_key = None, 
				 warnings = True):

		from powerbpy.dataset_csv import BlobCsv

		dataset = BlobCsv(self,
				 data_path,
				 account_url, 
				 blob_name, 
				 tenant_id = None, 
				 use_saved_storage_key = False,  
				 SAS_url = None,
				 storage_account_key = None, 
				 warnings = True)
		
		self.datasets.append(dataset)
		return dataset

	def get_measures_list(dashboard_path, 
                      export_type = 'markdown', 
					  output_file_path = "", 
					  starts_with = 'formatString:'):
					  
		'''Returns a list of DAX measures in the report
		Parameters
		----------
		export_type: str
			Export type for the function result: export to a .xlsx file (parameter value 'xlsx'), to a .csv file (parameter value 'csv'), or output in markdown format without saving (parameter value 'markdown'')
		output_file_path: str
			The path for export (if the export_type value is specified as '.xlsx' or '.csv'). Example: "D:/PBI project/blank_template/", export result will be stored as "D:/PBI project/blank_template/blank_template - measures.xlsx""
		starts_with: str
			Technical parameter for measure selection. Default options is 'formatString:', for older reports without formatString in the measure definition try using 'lineageTag:' instead
			
		Returns
		-------
		Returns a list of DAX measures used in the report in the specified format (see param export_type): the measure name, its definition, the table it belongs to, and the description (if available); prints "Measures not found" otherwise
		'''
		
		items = os.listdir(self.tables_folder)
		
		measures = []
		capture_description = False
		
		for item in items:
			item_path = os.path.join(self.tables_folder, item)
			
			if item.endswith('.tmdl'):
				
				table_name = item.replace(".tmdl", "")
				
				try:
					with open(item_path, 'r', encoding='utf-8') as file:
						lines = file.readlines()
						
					in_measure = False
					buffer = []
						
					for line in lines:
						stripped = line.strip()
						
						# Capture description
						if stripped.startswith("///"):
							description_text = stripped.lstrip("/ ").strip()
							capture_description = True
							
						if stripped.startswith("measure ") and "=" in stripped:
							# Start of new measure
							in_measure = True
							buffer = [stripped]
							continue
							
						if in_measure:
							if stripped.startswith(starts_with):
								# End of measure expression, get flattened version
								join_buffer = ' '.join(buffer)
								
								current_measure = {}
								
								parts = join_buffer.split("=", 1)
								current_measure["name"] = parts[0].strip()
								current_measure["expression"] = parts[1].strip()
								current_measure["table"] = table_name
								
								# If description was just seen before measure
								if capture_description:
									current_measure["description"] = description_text
								else:
									current_measure["description"] = ""
								capture_description = False
								
								measures.append(current_measure)
								
								in_measure = False

							else:
								if stripped:
									buffer.append(stripped)
								
								
				except Exception as e:
					print(f"Error opening or reading file {item}: {e}")
					
		# Create DataFrame
		if len(measures)>0:
			df = pd.DataFrame(measures, columns=["name", "expression", "table", "description"])
			
			if export_type == 'xlsx':
				df.to_excel(f"{output_file_path}{self.report_name} - measures.xlsx")
				print("Export to .xlsx finished")
				
			elif export_type == 'csv':
				df.to_csv(f"{output_file_path}{self.report_name} - measures.csv")
				print("Export to .csv finished")
				
			elif export_type == 'markdown':
				print(df.to_markdown())
				
		else:
			print("Measures not found")



		



