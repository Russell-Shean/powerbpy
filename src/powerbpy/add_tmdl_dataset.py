import os, re, shutil

from pathlib import Path
from importlib import resources


import powerbpy.update_diagramLayout as PBI_DL
import powerbpy.update_model_file as PBI_model              # internal function to add data to model.tmdl



def add_tmdl_dataset(dashboard_path, data_path = None, add_default_datetable = True):

	'''Add a locally stored TMDL file to the dashboard       

	- TMDL is a data storage format automatically created by power BI consisting of a table and column definitions and the M code used to generate the dataset.        
	- In practice this means that you can copy datasets between dashboards. You can use this function to automatically copy the TMDL files at scale         
	- Potential pitfalls: M needs full paths to load data. If the new dashboard doesn't have access to the same data as the old dashboard, the data copying may fail.       

	Parameters        
	----------        
	dashboard_path: str        
	    The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders).        
	data_path: str        
	    The path where the tmdl file is stored.        
	add_default_datetable: boolean       
	    Do you want the TMDL file you add to be our team's custom date table? This will allow you to create your own date heirarchies instead of using time intelligence

	
	'''

	if data_path is not None and add_default_datetable is True:
		raise ValueError("If you are providing a path to a tmdl dataset, the add_default_datetable argument can't be set to True")	
	




	# file paths
	report_name = os.path.basename(dashboard_path)

	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	definitions_folder = os.path.join(semantic_model_folder, "definition")
	tables_folder = os.path.join(definitions_folder, 'tables')


	# create tables folder if it doesn't already exist
	if not os.path.exists(tables_folder):
		os.makedirs(tables_folder)


	# check to see if we're importing the default DateTable.tmdl file
	# if the add default datetable argument is true
	# we'll use the path to the default datetable instead of the user supplied data_path
	# for the path to the datable we're going to add
	if add_default_datetable and data_path is None:

		# define the path we'll move the table to
		tmdl_dataset_path = os.path.join(tables_folder, "DateTable.tmdl")
		dataset_name = "DataTable"
		

		data_path = str(resources.files("powerbpy.dashboard_resources.python_resources").joinpath("DateTable.tmdl"))


		# copy date table from package resources to table folder
		shutil.copy(data_path, tmdl_dataset_path)

		# change the data_path to be the newly copied file
		data_path = tmdl_dataset_path

	else:
		# define the path we'll move the table to
		tmdl_dataset_path = os.path.join(tables_folder, os.path.basename(data_path))

		# dateset_name
		# extract the dataset name from the tmdl file's path
		# extract bits of names for later
		path_end = os.path.basename(data_path)
		split_end = os.path.splitext(path_end)

		dataset_name = split_end[0]

		# otherwise we move the tmdl file defined by the user to the tables folder
		# add the new tmdl file to the tables folder
		shutil.move(data_path, tmdl_dataset_path)





	# dateset_name -----------------------------------------------------------------------------------------------
	# read the whole table.tmdl file in andmake it a giant blob for regex
	file_content = ""

	with open(data_path) as file: 

		# list comprehension
		# all lines have all the white spaces and \n and \t striped 
		# They're then joined together using the .join function and ~ as a seperator
		file_content = "~".join(re.sub('\t?', '', line).rstrip() for line in file)


	# pull out just the dataset_id using regex
	m = re.search("(?<=lineageTag: ).*?(?=~~column)", file_content )


	dataset_id = m.group(0)




	# update the diagramLayout file to include the new date table\
	PBI_DL.update_diagramLayout(dashboard_path = dashboard_path, dataset_name = dataset_name, dataset_id = dataset_id)

	# update the model.tmdl file to include the new datetable
	PBI_model.update_model_file(dashboard_path = dashboard_path, dataset_name = dataset_name)



