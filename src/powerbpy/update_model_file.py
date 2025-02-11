# modify modil tmdl
import re, shutil, os

def update_model_file(dashboard_path, dataset_name):

	'''
	This is an internal function to add a dataset to the model.tmdl file when a new dataset is added. 
	It assumes you want the new dataset to be loaded last. 

	:param str dashboard_path The path to the top level folder where you store all the report's files.
	:param str dataset_name The name of the dataset you are adding
	return None



	'''


	# file paths
	report_name = os.path.basename(dashboard_path)

	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	definitions_folder = os.path.join(semantic_model_folder, "definition")
	model_path = os.path.join(definitions_folder, 'model.tmdl')
	temp_model_path = os.path.join(dashboard_path, 'model2.tmdl')


	# loop through all the lines in the model file
	# to find that part that lists the order of the datasets

	with open(temp_model_path, 'w') as tmp:
		with open(model_path, "r") as file:
			for line in file.readlines():

				# check to see if the line is the one we want
				m = re.search("(?<=annotation PBI_QueryOrder = ).*", line)

				# if it is, read the list of datasets and append a new one in

				if m is not None:
					# execute the tmdl code to make a python list

					# execute the code (including local and global scopes)
					# source: https://stackoverflow.com/questions/41100196/exec-not-working-inside-function-python3-x
					exec(f'query_order_list = {m.group(0)}', locals(), globals())

					# add the dataset using python method then write back  to line
					query_order_list.append(dataset_name)
					line = f'annotation PBI_QueryOrder = {query_order_list}\n'

					# write back the line to a temporary file

				tmp.write(line)

			# append the dataset name at the end of the file
			tmp.write(f"\n\nref table {dataset_name}")


  # Replace the model file with the temp file we created
	shutil.move(temp_model_path, model_path)


