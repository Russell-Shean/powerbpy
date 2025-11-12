import pandas as pd
import os, uuid, json, re, shutil

# Import a custom function to create the date heirarchies
import powerbpy as PBI

def add_local_csv(dashboard_path, data_path, save_data_copy=True):

	'''Add a locally stored CSV file to a dashboard
	
	:param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
	:param str data_path: The path where the csv file is stored. Can be a relative path. The M code requires a full path, but this python function will help you resolve any valid relative paths to an absolute path.  
	:param bool save_data_copy: Do you want to store a copy of the data in the dashboard's project folder. This is important for some functions such as add_sanky_chart

	:returns: dataset_id: A randomly generated UUID that you can use to reference the datset. 

	The dataset path must be full (not relative path.) If using a relative path for the dashboard_path, the path must be within the current working directory. 
	This function creates custom M code and is therefore more picky than pandas or Power BI desktop. 
	The csv file should probably not have row numbers. (Any column without a column name will be renamed to "probably_an_index_column")
	NA values must display as "NA" or "null" not as N/A. 
	If the data is malformed in Power BI, try cleaning it first in python and then rerunning this function. 

	This function creates a new TMDL file defining the dataset in TMDL format and also in M code.
	The DiagramLayout and Model.tmdl files are updated to include refrences to the new dataset. 

	'''

  # generate a random id for the data set
	dataset_id = str(uuid.uuid4())


	# extract bits of names for later
	path_end = os.path.basename(data_path)
	split_end = os.path.splitext(path_end)

	dataset_name = split_end[0]
	dataset_extension = split_end[1]


	report_name = os.path.basename(dashboard_path)


	# Convert the user provided data_path to a relative path
	# because Power BI requires it...
	data_path = os.path.abspath(os.path.expanduser(data_path))



  # Reverse slash directions bc windows
	data_path_reversed = data_path.replace('/', '\\')
	


	# file paths
	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	definitions_folder = os.path.join(semantic_model_folder, "definition")
	model_path = os.path.join(definitions_folder, 'model.tmdl')
	temp_model_path = os.path.join(dashboard_path, 'model2.tmdl')

	relationships_path = os.path.join(definitions_folder, "relationships.tmdl")
	diagram_layout_path = os.path.join(semantic_model_folder, 'diagramLayout.json')

	tables_folder = os.path.join(definitions_folder, 'tables')
	dataset_file_path = os.path.join(tables_folder, f'{dataset_name}.tmdl')

	# create a tables folder if it doesn't already exist
	if not os.path.exists(tables_folder):
		os.makedirs(tables_folder)


	# load dataset using pandas
	dataset = pd.read_csv(data_path)

	# remove unnamed columns
	dataset.rename( columns={'Unnamed: 0':'probably_an_index_column'}, inplace=True )



	# add dataset to diagramLayout file ---------------------------------------------------------------------
	PBI.update_diagramLayout(dashboard_path = dashboard_path, dataset_name = dataset_name, dataset_id = dataset_id)


  # Call a function to update the model file with the dataset
	PBI.update_model_file(dashboard_path = dashboard_path, dataset_name = dataset_name)


	# Data model file --------------------------------------------------------------------------
	col_attributes = PBI.create_tmdl(dashboard_path = dashboard_path, dataset_name = dataset_name, dataset_id = dataset_id, dataset = dataset)



	# write out M code 
	# bc we're stilllllllll not done.....


	# for debugging:
	#print(f"column attributes:\n {col_attributes}\n\n")

	# define tricky bits of code
	replacement_values =  '", "'.join(col_attributes["col_names"]) 
	formatted_column_details = ', '.join(map(str, col_attributes["col_deets"]))


	# for debugging:
	#print(f"Replacement values:\n {replacement_values}\n\n")
	#print(f"formatted_column_details values:\n {formatted_column_details}\n\n")

	with open(dataset_file_path, 'a') as file:
		file.write(f'\tpartition {dataset_name} = m\n')
		file.write('\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n')
		file.write(f'\t\t\t\t\tSource = Csv.Document(File.Contents("{data_path_reversed}"),[Delimiter=",", Columns={len(dataset.columns)}, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n')
		file.write('\t\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n')
		file.write(f'\t\t\t\t\t#"Replaced Value" = Table.ReplaceValue(#"Promoted Headers","NA",null,Replacer.ReplaceValue,{{"{ replacement_values  }"}}),\n')
		file.write(f'\t\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Replaced Value",{{  {  formatted_column_details  }   }})\n')
		file.write('\t\t\t\tin\n\t\t\t\t\t#"Changed Type"\n\n')
		file.write('\tannotation PBI_ResultType = Table\n\n\tannotation PBI_NavigationStepName = Navigation\n\n')



	# return the dataset_id in case we need it later
	return dataset_id




'''More deugging
report_name = "blorg"
report_location = f"C:/Users/rps1303/PBI_projects"

dashboard_path = f"{report_location}/{report_name}"


col_attributes = add_csv(dashboard_path, "C:/Users/rps1303/Downloads/colony.csv" )

print(col_attributes)

'''

