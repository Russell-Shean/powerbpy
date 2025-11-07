# Create a new blank .pbir dashboard
import os, uuid, shutil, json

from pathlib import Path
from importlib import resources



def create_new_dashboard(parent_dir, report_name):

	'''Create a new dashboard in the specified folder      

	- This function creates a power BI report in the specified parent directory.          
	- The dashboard can be opened and edited in Power BI desktop like normal, or be further modified progromatically using other functions in this package.       
	- The function creates a folder with the name report_name inside parent_dir with all the dashboard's files.       
	- The dashboard uses a .pbip/.pbir format with TMDL enabled.        
	- To publish this type of dashboard you will need to either use git enabled workspaces OR convert to a .pbit template and then to a .pbix file before publishing       
	- These annoyances are worth it because the .pbir + TMDL format is the only one that allows real version control and programatic manipulation of the report using these functions.       
	- (.pbip uses mimified json by default and throws an error when it's given unpacked json).      

	- This dashboard turns off time intelligence and relationship autodection off by default      

	- If you have the option I would recommend looking into a different web development framework (shiny, flask, etc) for building dashboards. 
	Only use this package if you have to :D            
	          
	Parameters          
	----------         
	parent_dir: str           
	    The path to the directory where you want to store the new dashboard          
	report_name: str         
	    Name of the report.      
		
	Returns        
	-------        
	None

	'''


	#create a new logical id field
	# see this for explanation of what a UUID is: https://stackoverflow.com/a/534847 
	report_logical_id = str(uuid.uuid4())
	sm_logical_id = str(uuid.uuid4())

	# define page name
	page1_name = "page1"

    
    # Define file paths ------------------------------------------------------------------------------------
	# Outer level directory --------------------------------------------------------------------------------
	project_folder_path = os.path.join(parent_dir, report_name)

	pbip_file_path = os.path.join(project_folder_path, f'{report_name}.pbip')


	## Report folder -----------------------------------------------------------------
	report_folder_path = os.path.join(project_folder_path, f'{report_name}.Report')
	platform_file_path = os.path.join(report_folder_path,  ".platform")
	pbir_file_path = os.path.join(report_folder_path, 'definition.pbir')


	### definition folder -------------------------------------------------------------------------------------
	report_definition_folder = os.path.join(report_folder_path, 'definition')

	pages_folder = os.path.join(report_definition_folder, 'pages')
	pages_file_path = os.path.join(pages_folder, "pages.json")


	page1_folder = os.path.join(pages_folder, page1_name)
	page1_json_path = os.path.join(page1_folder, "page.json")



	## report_name.SemanticModel folder ----------------------------------------------------------------------------
	semantic_model_folder_path = os.path.join(project_folder_path, f'{report_name}.SemanticModel')
	sm_platform_file_path = os.path.join(semantic_model_folder_path, ".platform")




	# check to make sure parent directory exists
	if not os.path.exists(parent_dir):
		raise ValueError("The parent directory doesn't exist! Please create it and try again!")


	# make sure a report folder doesn't already exist
	if os.path.exists(project_folder_path):
		raise ValueError("Sorry a report with that name already exists! Please use a different report name or parent directory and try again")
	
	


	# Transfer all the blank dashboard files from the package resources ---------------------------------------------------


	traversable = resources.files("powerbpy.dashboard_resources")
	
	with resources.as_file(traversable) as path:
		shutil.copytree(path, project_folder_path)




	# Change file names -----------------------------------------------------------------------------------------------------
	os.rename(os.path.join(project_folder_path, "blank_template.Report"), report_folder_path)
	os.rename(os.path.join(project_folder_path, "blank_template.SemanticModel"), os.path.join(project_folder_path, f'{report_name}.SemanticModel'))

	os.rename(os.path.join(project_folder_path, "blank_template.pbip"), pbip_file_path)

	os.rename(os.path.join(project_folder_path, f'{report_name}.Report/definition/pages/915e09e5204515bccac2'), os.path.join(project_folder_path, f'{report_name}.Report/definition/pages/{page1_name}'))



	# Modify files --------------------------------------------------------------------



	## top level -----------------------------------------------------------------------


	# .pbip file
	with open(pbip_file_path,'r') as file:
		pbip_file = json.load(file)
    
    # modify the report path
	pbip_file["artifacts"][0]["report"]["path"] = f'{report_name}.Report'

	# write to file
	with open(pbip_file_path,'w') as file:
		json.dump(pbip_file, file, indent = 2)





	## report folder -----------------------------------------------------------------

	# .platform file
	with open(platform_file_path,'r') as file:
		platform_file = json.load(file)

    
    # modify the display name
	platform_file["metadata"]["displayName"] = f'{report_name}'


	# update the unique UUID
	platform_file["config"]["logicalId"] = report_logical_id

	# write to file
	with open(platform_file_path,'w') as file:
		json.dump(platform_file, file, indent = 2)



	#.pbir file
	with open(pbir_file_path,'r') as file:
		pbir_file = json.load(file)

    # modify the display name
	pbir_file["datasetReference"]["byPath"]["path"] = f'../{report_name}.SemanticModel'


	# write to file
	with open(pbir_file_path,'w') as file:
		json.dump(pbir_file, file, indent = 2)



	### definition folder --------------------------------------------------------

	# pages.json
	with open(pages_file_path,'r') as file:
		pages_file = json.load(file)


	pages_file["pageOrder"] = [page1_name]
	pages_file["activePageName"] = page1_name

	# write to file
	with open(pages_file_path,'w') as file:
		json.dump(pages_file, file, indent = 2)


	#### page 1 folder
	with open(page1_json_path,'r') as file:
		page1_json = json.load(file)


	page1_json["name"] = page1_name

	# write to file
	with open(page1_json_path,'w') as file:
		json.dump(page1_json, file, indent = 2)



	## Semantic model folder ----------------------------------------------------------------
	# .platform file
	with open(platform_file_path,'r') as file:
		platform_file = json.load(file)

    
    # modify the display name
	platform_file["metadata"]["displayName"] = f'{report_name}'


	# update the unique UUID
	platform_file["config"]["logicalId"] = sm_logical_id

	# write to file
	with open(platform_file_path,'w') as file:
		json.dump(platform_file, file, indent = 2)



	### definition folder


















