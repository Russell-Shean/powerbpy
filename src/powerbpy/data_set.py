''' A generic class representing datasets. Currently it is called by local and blob csv files, but not TMDL datasets'''

import os
import uuid
import json
import re
import shutil
import ast

import pandas as pd # pylint: disable=import-error

from powerbpy.dashboard import Dashboard

class _DataSet:

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-instance-attributes

    # Get everything else from the dashboard
    # Attribute delegation (inherit parent instance attributes)

    def __init__(self,
                 dashboard,
                 data_path,
                 dataset_id=None):


        ''' A generic class representing datasets. Currently it is called by local and blob csv files, but not TMDL datasets
        '''



        if not isinstance(dashboard, Dashboard):
            raise TypeError("Datasets must be attached to a Dashboard instance")


        self.dashboard = dashboard
        self.data_path = os.path.abspath(os.path.expanduser(data_path))

        # generate a random id for the data set
        if dataset_id is None:
            self.dataset_id = str(uuid.uuid4())
        else:
            self.dataset_id = dataset_id

        # extract bits of names for later
        self.path_end = os.path.basename(self.data_path)
        self.split_end = os.path.splitext(self.path_end)

        self.dataset_name = self.split_end[0]
        self.dataset_extension = self.split_end[1]

        # Reverse slash directions bc windows
        self.data_path_reversed = self.data_path.replace('/', '\\')

        # file paths
        self.dataset_file_path = os.path.join(self.dashboard.tables_folder, f'{self.dataset_name}.tmdl')

        # create a tables folder if it doesn't already exist
        if not os.path.exists(self.dashboard.tables_folder):
            os.makedirs(self.dashboard.tables_folder)


        # add dataset to diagramLayout file ---------------------------------------------------------------------
        with open(self.dashboard.diagram_layout_path,'r', encoding="utf-8") as file:
            self.diagram_layout = json.load(file)

        # add all this junk to describe the table's "nodes"
        self.diagram_layout["diagrams"][0]["nodes"].append(
                {
                    "location": {
                        "x": 0,
                        "y": 0
                        },
                    "nodeIndex": self.dataset_name,
                    "nodeLineageTag": self.dataset_id,
                    "size": {
                        "height": 300,
                        "width": 234
                        },
                    "zIndex": 0
                    }
                    )

        # write to file
        with open(self.dashboard.diagram_layout_path,'w', encoding="utf-8") as file:
            json.dump(self.diagram_layout, file, indent = 2)

        # update the model file with the dataset--------------------------------------------------------------------
        # loop through all the lines in the model file
        # to find that part that lists the order of the datasets
        with open(self.dashboard.temp_model_path, 'w', encoding="utf-8") as tmp:
            with open(self.dashboard.model_path, "r", encoding="utf-8") as file:
                for line in file.readlines():

                    # check to see if the line is the one we want
                    m = re.search("(?<=annotation PBI_QueryOrder = ).*", line)

                    # if it is, read the list of datasets and append a new one in

                    # execute the tmdl code to make a python list


                    if m is not None:

                        # execute the code (including local and global scopes)
                        # source: https://stackoverflow.com/questions/41100196/exec-not-working-inside-function-python3-x
                        query_order_list = ast.literal_eval(m.group(0))

                        # add the dataset using python method then write back  to line
                        query_order_list.append(self.dataset_name)
                        line = f'annotation PBI_QueryOrder = {query_order_list}\n'

                    # write back the line to a temporary file
                    tmp.write(line)

                # append the dataset name at the end of the file
                tmp.write(f"\n\nref table {self.dataset_name}")

        # Replace the model file with the temp file we created
        shutil.move(self.dashboard.temp_model_path, self.dashboard.model_path)


    # Data model file --------------------------------------------------------------------------
    def _create_tmdl(self):
        # pylint: disable=no-member
        # pylint: disable=too-many-branches, too-many-statements

        '''An internally called function that creates a TMDL file from a pandas dataframe
        Parameters
        ----------
        dataset_name: str
            The name of the dataset. This should be the basename of the original file without the extension. For example if you loaded "%userprofile%/documents/datasets/birds.csv", the dataset name would be "birds".
        dataset_id: str
            The dataset's UUID, this will be generated by the outer level function that calls create_tmdl().
        dataset: DataFrame
            This is a pandas dataframe of the csv's content. The pd.read_csv() function is called by the outer level function that calls create_tmdl().

        Returns
        -------
        col_attributes: dict
            A dictionary containing the name and type of all the columns in the dataset. This is needed to get the M code in the outer level function to work.

        Notes
        -----
        This function loops through all the dataframe's columns, checks the column's type (text, number, date), and generates the appropriate TMDL column definition for that type.
        Dates will only be recocognized as dates if they are in the format (YYYY-MM-DD) i.e. (1999-12-31). If your date is in another format please change in python before calling the add_csv functions.
        '''

        self.col_names = []
        self.col_deets = []
        self.col_attributes = {}

        self.dataset.rename( columns={'Unnamed: 0':'probably_an_index_column'}, inplace=True )

        # sink inital header stuff about dataset
        with open(self.dataset_file_path, 'w', encoding="utf-8") as file:
            file.write(f'table {self.dataset_name}\n\tlineageTag: {self.dataset_id}\n\n')

        # read in the dataset
        # compare how pandas manages to do this in a single line
        # and Power BI requires 40 lines of code and modifying multiple files to do the same thing
        # sooo, that's a thing........
        for col in self.dataset:

            # Loop through the dataset and find dates
            for value in self.dataset[col][0:100]:
                m = re.search("^\\d{4}-\\d{2}-\\d{2}$", str(value))

                if m is not None:
                    #print(f"{col}: This column is probably a date!")

                    # change the data type in the panda dataframe
                    self.dataset[col] = pd.to_datetime(self.dataset[col], format = "%Y-%m-%d")
                    break

        # loop through columns and write specs out to model file
        for col in self.dataset:

            # convert unnambed columns back to "", but only for m code not tmdl code
            # why? bc msft....
            if col == "probably_an_index_column":
                col_for_m = ""
            else:
                col_for_m = col


            # loop through the values in a column to see if it contains dates
            # Loop through the dataset and find dates
            for value in self.dataset[col][0:100]:
                m = re.search("^\\d{4}-\\d{2}-\\d{2}$", str(value))

                if m is not None:
                    #print(f"{col}: This column is probably a date!")

                    # change the data type in the panda dataframe
                    self.dataset[col] = pd.to_datetime(self.dataset[col], format = "%Y-%m-%d")


            # add the column's name to a set for later
            self.col_names.append(col)

            # record more details in a different set
            col_id = str(uuid.uuid4())

            # For numbers, we're not distinguishing between integers (int64)
            # and numbers (double)
            if self.dataset[col].dtype in ("int64", "float64"):

                # record more details in a different set
                self.col_deets.append(f'{{"{col_for_m}", type number}}')

                with open(self.dataset_file_path, 'a', encoding="utf-8") as file:
                    file.write(f"\tcolumn '{col}'\n")
                    file.write('\t\tdataType: double\n')
                    file.write(f'\t\tlineageTag: {col_id}\n')
                    file.write('\t\tsummarizeBy: sum\n')
                    file.write(f'\t\tsourceColumn: {col}\n\n')
                    file.write('\t\tannotation SummarizationSetBy = Automatic\n\n')
                    file.write('\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}\n\n')


            # strings ------------------------------------------------
            if self.dataset[col].dtype == "object":

                # record more details in a different set
                self.col_deets.append(f'{{"{col_for_m}", type text}}')


                with open(self.dataset_file_path, 'a', encoding="utf-8") as file:
                    file.write(f"\tcolumn '{col}'\n")
                    file.write('\t\tdataType: string\n')
                    file.write(f'\t\tlineageTag: {col_id}\n')
                    file.write('\t\tsummarizeBy: none\n')
                    file.write(f'\t\tsourceColumn: {col}\n\n')
                    file.write('\t\tannotation SummarizationSetBy = Automatic\n\n')

            # dates ----------------------------------------------
            if self.dataset[col].dtype == "datetime64[ns]":

                # record more details in a different set
                self.col_deets.append(f'{{"{col_for_m}", type date}}')

                with open(self.dataset_file_path, 'a', encoding="utf-8") as file:
                    file.write(f"\tcolumn '{col}'\n")
                    file.write('\t\tdataType: dateTime\n')
                    file.write('\t\tformatString: Long Date\n')
                    file.write(f'\t\tlineageTag: {col_id}\n')
                    file.write('\t\tsummarizeBy: none\n')
                    file.write(f'\t\tsourceColumn: {col}\n\n')
                    file.write('\t\tannotation SummarizationSetBy = Automatic\n\n')
                    file.write('\t\tannotation UnderlyingDateTimeDataType = Date\n\n')



        # create a dictionary containing col_deets and col_names
        self.col_attributes = {"col_deets":self.col_deets, "col_names": self.col_names}
        return self.col_attributes
