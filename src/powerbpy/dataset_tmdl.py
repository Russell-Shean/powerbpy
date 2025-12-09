'''This class is used to represent TMDL datasets that can be added to dashboards.
    You should never call this class directly, instead use the add_tmdl() method attached to the Dashboard class.
'''

import shutil
import re
import os
import ast

import json

from importlib import resources

class _Tmdl:

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals

    def __init__(self,
                 dashboard,
                 data_path = None,
                 add_default_datetable = True):

        '''Add a locally stored TMDL file to the dashboard

        Parameters
        ----------
        data_path: str
            The path where the tmdl file is stored.
        add_default_datetable: bool
            Do you want the TMDL file you add to be our team's custom date table? This will allow you to create your own date heirarchies instead of using time intelligence

        Notes
        -----
        - TMDL is a data storage format automatically created by power BI consisting of a table and column definitions and the M code used to generate the dataset.
        - In practice this means that you can copy datasets between dashboards. You can use this function to automatically copy the TMDL files at scale
        - Potential pitfalls: M needs full paths to load data. If the new dashboard doesn't have access to the same data as the old dashboard, the data copying may fail.

        '''


        self.dashboard = dashboard

        if data_path is not None and add_default_datetable is True:
            raise ValueError("If you are providing a path to a tmdl dataset, the add_default_datetable argument can't be set to True")


        # check to see if we're importing the default DateTable.tmdl file
        # if the add default datetable argument is true
        # we'll use the path to the default datetable instead of the user supplied data_path
        # for the path to the datable we're going to add
        if add_default_datetable and data_path is None:

            # define the path we'll move the table to
            tmdl_dataset_path = os.path.join(self.dashboard.tables_folder, "DateTable.tmdl")
            self.dataset_name = "DataTable"

            data_path = str(resources.files("powerbpy.dashboard_resources.python_resources").joinpath("DateTable.tmdl"))

            # copy date table from package resources to table folder
            shutil.copy(data_path, tmdl_dataset_path)

            # change the data_path to be the newly copied file
            data_path = tmdl_dataset_path

        else:

            # define the path we'll move the table to
            tmdl_dataset_path = os.path.join(self.dashboard.tables_folder, os.path.basename(data_path))

            # dateset_name
            # extract the dataset name from the tmdl file's path
            # extract bits of names for later
            path_end = os.path.basename(data_path)
            split_end = os.path.splitext(path_end)

            self.dataset_name = split_end[0]

            # otherwise we move the tmdl file defined by the user to the tables folder
            # add the new tmdl file to the tables folder
            shutil.move(data_path, tmdl_dataset_path)


        # dateset_name -----------------------------------------------------------------------------------------------
        # read the whole table.tmdl file in andmake it a giant blob for regex
        file_content = ""

        with open(data_path, encoding="utf-8") as file:
            # list comprehension
            # all lines have all the white spaces and \n and \t striped
            # They're then joined together using the .join function and ~ as a seperator
            file_content = "~".join(re.sub('\t?', '', line).rstrip() for line in file)


        # pull out just the dataset_id using regex
        m = re.search("(?<=lineageTag: ).*?(?=~~column)", file_content )

        self.dataset_id = m.group(0)


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
