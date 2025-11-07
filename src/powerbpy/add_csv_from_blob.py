from azure.storage.filedatalake import DataLakeFileClient
from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobClient

import pandas as pd
import keyring, getpass, re, os, uuid, warnings

# Import function to update the model.tmdl file
import powerbpy.update_model_file as PBI_model              # internal function to add data to model.tmdl
import powerbpy.update_diagramLayout as PBI_DL
import powerbpy.create_tmdl as PBI_TMDL


def add_csv_from_blob(dashboard_path, 
    account_url, 
    blob_name, 
    data_path, 
    tenant_id = None, 
    use_saved_storage_key = False,  
    SAS_url = None,
    storage_account_key = None, 
    warnings = True):

    '''Add a csv file store in a ADLS blob container to a dashboard

    DO NOT HARD CODE CREDENTIALS. Use the use_saved_storage_key option instead.

    This function creates custom M code and is therefore more picky than pandas or Power BI desktop. 
    The csv file should probably not have row numbers. (Any column without a column name will be renamed to "probably_an_index_column")
    NA values must display as "NA" or "null" not as N/A. 
    If the data is malformed in Power BI, try cleaning it first in python and then rerunning this function. 

    This function creates a new TMDL file defining the dataset in TMDL format and also in M code.
    The DiagramLayout and Model.tmdl files are updated to include refrences to the new dataset.
    Other dumb things: If you get an error when trying to open the .pbip file try changing the combatibility version to 1567 in the semanticmodel > definition > database.tmdl file. 
    Thanks Microsoft for yet again doing a great job with backward compatibility lol. 
    Dashboards created with the create_blank_dashboard() function start with the compatibility version set to 1567, so you should only have this problem with manually created dashboards. 
    I may eventually add an automatic fix for this. 

    :param str dashboard_path: The path where the dashboard files are stored. (This is the top level directory containing the .pbip file and Report and SemanticModel folders).
    :param str account_url: The url to your Azure storage account. It should be in the format of https://<YOUR STORAGE ACCOUNT NAME>.blob.core.windows.net/. You can find it in Azure Storage Explorer by clicking on the storage account and then looking at the blob endpoint field
    :param str blob_name: The name of the blob container. In Azure Storage Explorer, click on the storage account, then inside "Blob Containers" will be all your blob containers. Use the node dislay name field. 
    :param str data_path: The relative path to the file you want to load from the blob. It should be relative to blob_name
    :param str tenant_id: The tenant id of the tenant where your storage account is stored. This field is only used with browser authentication. (The default).
    :param boolean use_saved_storage_key: This optional argument tells python to look in your system's default credential manager for an Azure Storage Account token and prompt the user to add one if it's not there. USE WITH CAUTION, THE STORAGE ACCOUNT TOKENS ALLOW FOR A MASSIVE AMOUNT OF ACCESS. CONSIDER USING SAS URLS OR INTERACTIVE BROWSER AUTHENTICATION INSTEAD.
    :param str SAS_url: A limited time single access url scoped to just the file you want to grant read access to. To generate one from Azure Storage Explorer, right click on the file you want and then choose "Get Shared Access Signature"
    :param str storage_account_key: Please, Please, Please do not use this when running this function on a local computer. Hardcoding credentials into code is SUPER BAD practice. Please set use_saved_storage_key to true instead. It will store the key securely in your operating system's credential manger. You should only pass a storage account key to the function if you are running this code in a cloud environment such as databricks and using that cloud platform's secure secret manager. (Something like Github Secrets or Azure Key Vault)

    :returns: None

    '''


    # file paths
    report_name = os.path.basename(dashboard_path)

    path_end = os.path.basename(data_path)
    split_end = os.path.splitext(path_end)

    dataset_name = split_end[0]

    semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
    definitions_folder = os.path.join(semantic_model_folder, "definition")
    tables_folder = os.path.join(definitions_folder, 'tables')
    dataset_file_path = os.path.join(tables_folder, f'{dataset_name}.tmdl')

    semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
    definitions_folder = os.path.join(semantic_model_folder, "definition")

    

    # generate a random id for the data set
    dataset_id = str(uuid.uuid4())

    # get the account name from the url
    m = re.search("(?<=https://).*(?=\\.blob)", account_url)

    account_name = m.group(0)


    if warnings:
        if storage_account_key is not None:
            warnings.warn("DO NOT HARD CODE CREDENTIALS!! Only provide a storage_account_key argument if you're securely retreiving it from something like azure key vault. If this code is running locally set use_saved_storage_key to true instead. Set warnings = False to disable this warning. ")



    if SAS_url is not None and use_saved_storage_key is True:
        raise ValueError("You can't save an azure storage key to your system's credential manager when providing an SAS_url. Try changing use_saved_storage_key to False and try again")


    if use_saved_storage_key is False:

        if tenant_id is None:
            raise ValueError("You must provide a tenant_id when using interactive browser authentication. (This function's default method of authentication). Please either provide a tenant id or use a different authentication type. ")

        credential = InteractiveBrowserCredential(
            tenant_id= tenant_id
            )

        file_handle = DataLakeFileClient(
            account_url=account_url,
            credential=credential,
            file_system_name=blob_name,
            file_path=data_path
            )


        download = file_handle.download_file()
        dataset = pd.read_csv(download)

    elif SAS_url is not None:

        print("You provided an SAS url!")
        dataset = pd.read_csv(SAS_url)


    else:

        # retrieve the storage token
        account_token = keyring.get_password('azure_account_key', 'token')

        # if no storage token was found, prompt the user for it
        if not account_token:

            add_key = "No key has been added yet..."

            while add_key != "y" and add_key != "n":
                add_key = input("Would you like to add an Azure Storage Container Key to your operating system's default credential manager?(y/n): ")

            if add_key == "n":
                raise ValueError("Loading files from azure requires using either an account_key, a SAS_url, or an interactive browser login.\nPlease change use_saved_storage_key to 'True', allow the system to store an azure_account_key, or provide an SAS_url")

            if add_key == "y":
                user_provided_key =  getpass.getpass(prompt="Please provide an Azure Storage Account Key: ", stream=None)

                # strip out white space
                user_provided_key = user_provided_key.strip()

                # test to make sure it's a reasonable key?....


                keyring.set_password('azure_account_key', 'token', user_provided_key)

                # Retrieve the stored API token
                account_token = keyring.get_password('azure_account_key', 'token')


        

        credential = {
                "account_name": account_name,
                "account_key": account_token}




        # read the data using the storage token
        file_handle = DataLakeFileClient(
            account_url=account_url,
            credential= credential,
            file_system_name=blob_name,
            file_path=data_path
            )


        download = file_handle.download_file()
        dataset = pd.read_csv(download)


    # rename unnamed columns
    dataset.rename( columns={'Unnamed: 0':'probably_an_index_column'}, inplace=True )



    # Add the dataset to dashboard
    # add dataset to diagramLayout file ---------------------------------------------------------------------
    PBI_DL.update_diagramLayout(dashboard_path = dashboard_path, dataset_name = dataset_name, dataset_id = dataset_id)


    # Call a function to update the model file with the dataset
    PBI_model.update_model_file(dashboard_path = dashboard_path, dataset_name = dataset_name)


    # Data model file --------------------------------------------------------------------------
    col_attributes = PBI_TMDL.create_tmdl(dashboard_path = dashboard_path, dataset_name = dataset_name, dataset_id = dataset_id, dataset = dataset)

    #print(col_attributes)


    # write out M code 
    # define tricky bits
    formatted_column_details = ', '.join(map(str, col_attributes["col_deets"]))
    with open(dataset_file_path, 'a') as file:
        file.write(f'\tpartition {dataset_name} = m\n')
        file.write('\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n')
        file.write(f'\t\t\t\t\tSource = AzureStorage.Blobs("{account_url}"),\n')
        file.write(f'\t\t\t\t\t#"{blob_name}1" = Source{{[Name="{blob_name}"]}}[Data],\n')
        file.write(f'\t\t\t\t\t#"https://{account_name} blob core windows net/{blob_name}/_{data_path.replace(".csv", "")} csv" = #"{blob_name}1"{{[#"Folder Path"="{account_url}/{blob_name}/",Name="{data_path}"]}}[Content],\n')
        file.write(f'\t\t\t\t\t#"Imported CSV" = Csv.Document(#"https://{account_name} blob core windows net/{blob_name}/_{data_path.replace(".csv", "")} csv",[Delimiter=",", Columns={len(dataset.columns)}, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n')
        file.write(f'\t\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true]),\n')
        file.write(f'\t\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{{ formatted_column_details }}})\n')
        file.write('\t\t\t\tin\n\t\t\t\t\t#"Changed Type"\n\n')
        file.write('\tchangedProperty = Name\n\n\tannotation PBI_ResultType = Table\n\n\tannotation PBI_NavigationStepName = Navigation\n\n')






