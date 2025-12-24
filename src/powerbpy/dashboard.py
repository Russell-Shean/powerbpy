'''Use these methods to create new dashboard, load existing dashboards, add datasets to the dashboard, and get information about pages and measures'''

import os
import uuid
import shutil
import json

from importlib import resources

import pandas as pd # pylint: disable=import-error

class Dashboard:
    '''A python class used to model a power BI dashboard project

    Notes
    -----
    - For clarity, avoid initiating a dashboard directly using `Dashboard(file_path)`, instead use `Dashboard.create()` or `Dashboard.load()`.
    - To create a new dashboard instance, use either `Dashboard.create(dashboard_path)` to create a new dashboard or `Dashboard.load(dashboard_path)` to load an existing dashboard.
    - The dashboard uses a .pbip/.pbir format with TMDL enabled.
    - Publishing .pbip files can be complicated. For more details see the [publishing section](https://www.russellshean.com/powerbpy/dashboard_publishing.html) of the Power Bpy website.
    - Time intelligence and relationship autodection are turned off by default

    '''
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=import-outside-toplevel

    def __init__(self,
                 file_path):
        '''A python class used to model a power BI dashboard project
        '''

        # Define pages as a list of instances of the page class
        self.pages = []

        self.datasets = []

        # Attributes calculated from what the user provides
        # create a new logical id field
        # see this for explanation of what a UUID is: https://stackoverflow.com/a/534847
        self.report_logical_id = str(uuid.uuid4())
        self.sm_logical_id = str(uuid.uuid4())

        # The parent directory should be converted to a full path
        # Because Power BI gets weird with relative paths

        # Define file paths ------------------------------------------------------------------------------------
        # Outer level directory --------------------------------------------------------------------------------
        self.project_folder_path = os.path.abspath(os.path.expanduser(file_path))
        self.report_name = os.path.basename(self.project_folder_path)
        self.parent_dir = os.path.dirname(self.project_folder_path)

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

        ## report_name.SemanticModel folder ----------------------------------------------------------------------------
        self.semantic_model_folder_path = os.path.join(self.project_folder_path, f'{self.report_name}.SemanticModel')
        self.sm_platform_file_path = os.path.join(self.semantic_model_folder_path, ".platform")

        self.sm_definition_folder = os.path.join(self.semantic_model_folder_path, "definition")

        self.model_path = os.path.join(self.sm_definition_folder, 'model.tmdl')
        self.temp_model_path = os.path.join(self.project_folder_path, 'model2.tmdl')

        self.diagram_layout_path = os.path.join(self.semantic_model_folder_path, 'diagramLayout.json')
        self.tables_folder = os.path.join(self.sm_definition_folder, 'tables')

    @classmethod
    def create(cls, file_path):

        '''Create a new dashboard     
        Parameters
        ----------
        file_path: str       
            The path to the directory where you want to store the new dashboard. The directory should not exist yet. The basename of the directory will also be the report name.

        Returns
        -------
        An instance of the dashboard class

        Notes
        -----
        - To create a new dashboard instance, use this function `Dashboard.create(dashboard_path)`
        - To load an existing dashboard use `Dashboard.load(dashboard_path)`    
           
        Here's an example:     
        ```python
        my_dashboard = Dashboard.create(dashboard_path)
        ```

        '''

        self = cls(file_path)

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

        # Delete the first page so that we can create a new page one with the new_page() method
        default_first_page = os.path.join(self.project_folder_path,
                                          f'{self.report_name}.Report/definition/pages/915e09e5204515bccac2')

        shutil.rmtree(default_first_page)

        # Modify files --------------------------------------------------------------------
        ## top level -----------------------------------------------------------------------
        # .pbip file
        with open(self.pbip_file_path,'r', encoding="utf-8") as file:
            pbip_file = json.load(file)

        # modify the report path
        pbip_file["artifacts"][0]["report"]["path"] = f'{self.report_name}.Report'

        # write to file
        with open(self.pbip_file_path,'w', encoding="utf-8") as file:
            json.dump(pbip_file, file, indent = 2)

        ## report folder -----------------------------------------------------------------
        # .platform file
        with open(self.platform_file_path,'r', encoding="utf-8") as file:
            platform_file = json.load(file)

        # modify the display name
        platform_file["metadata"]["displayName"] = f'{self.report_name}'

        # update the unique UUID
        platform_file["config"]["logicalId"] = self.report_logical_id

        # write to file
        with open(self.platform_file_path,'w', encoding="utf-8") as file:
            json.dump(platform_file, file, indent = 2)

        #.pbir file
        with open(self.pbir_file_path,'r', encoding="utf-8") as file:
            pbir_file = json.load(file)

        # modify the display name
        pbir_file["datasetReference"]["byPath"]["path"] = f'../{self.report_name}.SemanticModel'

        # write to file
        with open(self.pbir_file_path,'w', encoding="utf-8") as file:
            json.dump(pbir_file, file, indent = 2)

        ### definition folder --------------------------------------------------------
        # pages.json
        with open(self.pages_file_path,'r', encoding="utf-8") as file:
            pages_file = json.load(file)

        pages_file["pageOrder"] = []
        pages_file["activePageName"] = "page1"

        # write to file
        with open(self.pages_file_path,'w', encoding="utf-8") as file:
            json.dump(pages_file, file, indent = 2)

        ## Semantic model folder ----------------------------------------------------------------
        # .platform file
        with open(self.platform_file_path,'r', encoding="utf-8") as file:
            platform_file = json.load(file)

        # modify the display name
        platform_file["metadata"]["displayName"] = f'{self.report_name}'

        # update the unique UUID
        platform_file["config"]["logicalId"] = self.sm_logical_id

        # write to file
        with open(self.platform_file_path,'w', encoding="utf-8") as file:
            json.dump(platform_file, file, indent = 2)

        return self


    @classmethod
    def load(cls,
             file_path):

        '''Load an existing dashboard from a file path

        Parameters
        ----------
        file_path: str        
            The path to the directory where you want to store the new dashboard. The directory should not exist yet. The basename of the directory will also be the report name.

        Returns
        -------
        An instance of the Dashboard class.

        Notes
        -----
        - To load an existing dashboard, use this function `Dashboard.load(dashboard_path)`.
        - To create a new dashboard use `Dashboard.create(dashboard_path)`.
        '''

        self = cls(file_path)

        # check to make sure that the dashboard seems to be an actual power BI dashboard
        for path in [self.report_folder_path,
                     self.semantic_model_folder_path,
                     self.pbip_file_path]:
            if not os.path.exists(path):
                raise ValueError("path doesn't exist! Confirm that the file path you provided is to a valid Power BI project folder")

        return self


    def new_page(self,
                 page_name,
                 title = None,
                 subtitle = None,
                 display_option = 'FitToPage'):
        '''Create a new blank dashboard page

        Parameters
        ----------
        page_name: str
            The display name for the page you just created. This is different from the page_id which is only used internally.
        title: str
            Title to put at the top of the page. This under the hood calls the add_text_box() function. If you would like more control over the title's appearance use that function instead.
        subtitle: str
            Subtitle to put at the top of the page. This under the hood calls the add_text_box() function. If you would like more control over the title's appearance use that function instead.
        display_option: str
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
            my_dashboard.new_page(page_name = "Bee Colonies",
                       title= "The bees are in trouble!",
                       subtitle = "We're losing bee colonies")
        ```

        Here's what the new page looks like in Power BI Desktop
        ![New Page Example](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/new_page_example.png?raw=true "Example Page")
        '''
        # Local import avoids circular import at module load
        from powerbpy.page import _Page

        # Assign a page_id based on the number of current pages

        # determine number of pages
        with open(self.pages_file_path,'r', encoding="utf-8") as file:
            pages_list = json.load(file)

        # determine number of pages
        n_pages = len(pages_list["pageOrder"])

        # create a new page id based on existing number of pages
        page_id = f"page{n_pages + 1}"

        # add the new page id to the pageOrder list
        pages_list["pageOrder"].append(page_id)

        # write to file
        with open(self.pages_file_path,'w', encoding="utf-8") as file:
            json.dump(pages_list, file, indent = 2)

        # Create a new instance of a page
        page = _Page(self,
                 page_id=page_id)

        # create a new json file for the new page
        page_json = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.2.0/schema.json",
                      "name": page_id,
                      "displayName": page_name,
                      "displayOption": display_option,
                      "height": 720,
                      "width": 1280,
                      "objects":{}}

        # write to file
        with open(page.page_json_path, "w", encoding="utf-8") as file:
            json.dump(page_json, file, indent = 2)

        # Add title and subtitle if requested
        if title is not None:
            page.add_text_box(text = title,
                            visual_id= f"{page.page_id}_title",
                 height=68,
                   width=545,
                     x_position = 394,
                     y_position = 44)

        if subtitle is not None:
            page.add_text_box(text = subtitle,
                              visual_id= f"{page.page_id}_subtitle",
                 height=38,
                   width=300,
                     x_position = 500,
                     y_position = 93,
                     font_size = 14)

        self.pages.append(page)
        return page

    def load_page(self,
                  page_id):
        '''Load an existing page

        Parameters
        ----------
        page_id: str
            The page_id of the page you'd like to load.

        Returns
        -------
        _Page: class
            This returns an instance of the Page class corresponding to the page you just loaded.

        Notes
        ----
        You should use this function to load an existing page from a power BI report as an instance of the Page class. This lets you call Page methods such as those that add visuals.
        To list all page ids you can use `Dashboard.list_pages()`. You can also check the .pbip folder structure to find the page ids.
        '''
        # Local import avoids circular import at module load
        from powerbpy.page import _Page

        page = _Page(self,
                    page_id=page_id)

        self.pages.append(page)
        return page

    def list_pages(self):

        '''List all pages associated with a dashboard

        Parameters
        ----------
        None

        Returns
        -------
        pages: list
            A list of all the page_ids in the dashboard

        Notes
        ----
        Use this function to get a list of all the page_ids associated with a dashboard. The list of page_ids is determined from reading the `.Report` > `definition` > `pages` > `pages.json` file.
        In general you can assume that page_ids listed in the page.json match the folder names for each page.
        '''

        with open(self.pages_file_path,'r', encoding="utf-8") as file:
            pages_file = json.load(file)

        return pages_file["pageOrder"]

    def add_tmdl(self,
                 data_path = None,
                 add_default_datetable = True):

        '''Add a locally stored TMDL file to the dashboard

        Parameters
        ----------
        data_path: str
            The path where the tmdl file is stored.
        add_default_datetable: bool
            Do you want the  built in TMDL file containing a variety of date combinations? This will allow you to create your own date hierarchies instead of using time intelligence.

        Notes
        -----
        - TMDL is a data storage format automatically created by power BI consisting of a table and column definitions and the M code used to generate the dataset.
        - In practice this means that you can copy datasets between dashboards. You can use this function to automatically copy the TMDL files at scale
        - Potential pitfalls: M needs full paths to load data. If the new dashboard doesn't have access to the same data as the old dashboard, the data copying may fail.
        '''

        from powerbpy.dataset_tmdl  import _Tmdl

        tmdl = _Tmdl(self,
                    data_path,
                    add_default_datetable)

        self.datasets.append(tmdl)
        return tmdl

    def add_local_csv(self,
                      data_path):

        '''Add a locally stored CSV file to a dashboard

        Parameters
        ----------
        data_path: str
            The path where the csv file is stored. Can be a relative path. The M code requires a full path, but this python function will help you resolve any valid relative paths to an absolute path.

        Returns
        -------
        dataset: class
            An instance of the internal _LocalCsv dataset class

        Notes
        -----
        This function creates custom M code and is therefore more picky than pandas or Power BI desktop.
        The csv file should probably not have row numbers. (Any column without a column name will be renamed to "probably_an_index_column").
        NA values must display as "NA" or "null" not as N/A.
        If the data is malformed in Power BI, try cleaning it first in python and then rerunning this function.

        This function creates a new TMDL file defining the dataset in TMDL format and also in M code.
        The DiagramLayout and Model.tmdl files are updated to include refrences to the new dataset.
        '''

        from powerbpy.dataset_csv import _LocalCsv

        dataset = _LocalCsv(self,
                           data_path)

        self.datasets.append(dataset)
        return dataset

    # pylint: disable=too-many-arguments
    def add_blob_csv(self,
                *,
                 data_path,
                 account_url,
                 blob_name,
                 tenant_id = None,
                 use_saved_storage_key = False,
                 sas_url = None,
                 storage_account_key = None,
                 warnings = True):

        '''Add a csv file stored in a ADLS blob container to a dashboard

        Parameters
        ----------
        account_url: str
            The url to your Azure storage account. It should be in the format of `https://<YOUR STORAGE ACCOUNT NAME>.blob.core.windows.net/`. You can find it in Azure Storage Explorer by clicking on the storage account and then looking at the blob endpoint field.
        blob_name: str
            The name of the blob container. In Azure Storage Explorer, click on the storage account, then inside "Blob Containers" will be all your blob containers. Use the node dislay name field.
        data_path: str
            The relative path to the file you want to load from the blob. It should be relative to `blob_name`.
        tenant_id: str
            The tenant id of the tenant where your storage account is stored. This field is only used with browser authentication. (The default).
        use_saved_storage_key: bool
            This optional argument tells python to look in your system's default credential manager for an Azure Storage Account token and prompt the user to add one if it's not there.       
                
            USE WITH CAUTION, storage account tokens give a significant number of permissions. Consider using SAS urls or interactive browser authentication for more limited permissions instead.
        sas_url: str
            A limited time single access url scoped to just the file you want to grant read access to. To generate one from Azure Storage Explorer, right click on the file you want and then choose "Get Shared Access Signature".
        storage_account_key: str
            It is not recommended to use this when running this function on a local computer. Hardcoding credentials into code is a potential security risk. On a local computer, please set use_saved_storage_key to true instead. It will store the key securely in your operating system's credential manger.      
                  
            You should only pass a storage account key to the function if you are running this code in a cloud environment such as databricks and using that cloud platform's secure secret manager. (Something like Github Secrets or Azure Key Vault)

        Returns
        -------
        None

        Notes
        -----
        You should never need to hard code credentials into your script. Use the use_saved_storage_key option or a key manager instead.

        This function creates custom M code and is therefore more picky than pandas or Power BI desktop.
        The csv file should probably not have row numbers. (Any column without a column name will be renamed to "probably_an_index_column").
        NA values must display as "NA" or "null" not as N/A.
        If the data is malformed in Power BI, try cleaning it first in python and then rerunning this function.

        This function creates a new TMDL file defining the dataset in TMDL format and also in M code.
        The DiagramLayout and Model.tmdl files are updated to include refrences to the new dataset.      
            
        If you get an error when trying to open the .pbip file try changing the combatibility version to 1567 in the `semanticmodel` > `definition` > `database.tmdl` file.

        Dashboards created with the Dashboard.create() function start with the compatibility version set to 1567, so you should only have this problem with manually created dashboards.
        I may eventually add an automatic fix for existing dashboards that you load with `Dashboard.load()`.
        '''

        from powerbpy.dataset_csv import _BlobCsv

        dataset = _BlobCsv(self,
                 data_path = data_path,
                 account_url = account_url,
                 blob_name = blob_name,
                 tenant_id = tenant_id,
                 use_saved_storage_key = use_saved_storage_key,
                 sas_url = sas_url,
                 storage_account_key = storage_account_key,
                 warnings = warnings)

        self.datasets.append(dataset)
        return dataset


    def get_measures_list(self,
                      export_type = 'markdown',
                      output_file_path = "",
                      starts_with = 'formatString:'):

        '''Return a list of DAX measures in the report
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
        # pylint: disable=too-many-locals
        # pylint: disable=broad-exception-caught
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-branches, too-many-statements

        items = os.listdir(self.tables_folder)

        measures = []

        description_text = ""
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
