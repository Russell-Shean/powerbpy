import os
import pandas as pd

def get_measures_list(dashboard_path, export_type = 'markdown', output_file_path = "", starts_with = 'formatString:'):

	'''Returns a list of DAX measures in the report

	:param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders). 
	:param str export_type: Export type for the function result: export to a .xlsx file (parameter value 'xlsx'), to a .csv file (parameter value 'csv'), or output in markdown format without saving (parameter value 'markdown'')
	:param str output_file_path: The path for export (if the export_type value is specified as '.xlsx' or '.csv'). Example: "D:/PBI project/blank_template/", export result will be stored as "D:/PBI project/blank_template/blank_template - measures.xlsx""
	:param str starts_with: Technical parameter for measure selection. Default options is 'formatString:', for older reports without formatString in the measure definition try using 'lineageTag:' instead

	:returns: Returns a list of DAX measures used in the report in the specified format (see param export_type): the measure name, its definition, the table it belongs to, and the description (if available); prints "Measures not found" otherwise
	'''

	# file paths ---------------------------------------------------------------------------
	report_name = os.path.basename(dashboard_path)
	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	definitions_folder = os.path.join(semantic_model_folder, "definition")
	tables_folder = os.path.join(definitions_folder, 'tables')

	items = os.listdir(tables_folder)

	measures = []
	capture_description = False

	for item in items:
		item_path = os.path.join(tables_folder, item)

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
			df.to_excel(f"{output_file_path}{report_name} - measures.xlsx")
			print("Export to .xlsx finished")
		elif export_type == 'csv':
			df.to_csv(f"{output_file_path}{report_name} - measures.csv")
			print("Export to .csv finished")
		elif export_type == 'markdown':
			print(df.to_markdown())
	else:
		print("Measures not found")