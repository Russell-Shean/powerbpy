
import json, os

def update_diagramLayout(dashboard_path, dataset_name, dataset_id):

	'''
	This is an internal function to add a dataset to the diagramLayout file when a new dataset is added. 

	:param str dashboard_path The path to the top level folder where you store all the report's files.
	:param str dataset_name The name of the dataset you are adding
	:param str dataset_id The unique uuid that microsoft uses for the dataset. This is generated automatically within the add_data functions. 
	
	return None




	'''


	# file paths   --------------------------------------------------------
	report_name = os.path.basename(dashboard_path)
	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	definitions_folder = os.path.join(semantic_model_folder, "definition")

	diagram_layout_path = os.path.join(semantic_model_folder, 'diagramLayout.json')






	with open(diagram_layout_path,'r') as file:
		diagram_layout = json.load(file)


	# add all this junk to describe the table's "nodes"
	diagram_layout["diagrams"][0]["nodes"].append( 
        {
          "location": {
            "x": 0,
            "y": 0
          },
          "nodeIndex": dataset_name,
          "nodeLineageTag": dataset_id,
          "size": {
            "height": 300,
            "width": 234
          },
          "zIndex": 0
        }
      )

   
	# write to file
	with open(diagram_layout_path,'w') as file:
		json.dump(diagram_layout, file, indent = 2)


