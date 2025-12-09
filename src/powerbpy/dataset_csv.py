'''This class is used to represent csv datasets that can be added to dashboards.
    You should never call this class directly, instead use the add_local_csv() or add_blob_csv() methods attached to the Dashboard class.
'''


import getpass
import re
import keyring # pylint: disable=import-error

from azure.storage.filedatalake import DataLakeFileClient # pylint: disable=import-error
from azure.identity import InteractiveBrowserCredential # pylint: disable=import-error

import pandas as pd # pylint: disable=import-error

from powerbpy.data_set import _DataSet


class _LocalCsv(_DataSet):

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments

    def __init__(self,
                 dashboard,
                 data_path):

        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-locals

        super().__init__(dashboard,data_path)

        # load the dataset as a pandas dataframe
        self.dataset = pd.read_csv(self.data_path)

        # Build the tmdl file based on the method defined on the parent class
        self._create_tmdl()

        # write out M code

        # for debugging:
        #print(f"column attributes:\n {col_attributes}\n\n")

        # define tricky bits of code
        replacement_values =  '", "'.join(self.col_attributes["col_names"])
        formatted_column_details = ', '.join(map(str, self.col_attributes["col_deets"]))

        # for debugging:
        #print(f"Replacement values:\n {replacement_values}\n\n")
        #print(f"formatted_column_details values:\n {formatted_column_details}\n\n")

        with open(self.dataset_file_path, 'a', encoding="utf-8") as file:
            file.write(f'\tpartition {self.dataset_name} = m\n')
            file.write('\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n')
            file.write(f'\t\t\t\t\tSource = Csv.Document(File.Contents("{self.data_path_reversed}"),[Delimiter=",", Columns={len(self.dataset.columns)}, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n')
            file.write('\t\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n')
            file.write(f'\t\t\t\t\t#"Replaced Value" = Table.ReplaceValue(#"Promoted Headers","NA",null,Replacer.ReplaceValue,{{"{ replacement_values  }"}}),\n')
            file.write(f'\t\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Replaced Value",{{  {  formatted_column_details  }   }})\n')
            file.write('\t\t\t\tin\n\t\t\t\t\t#"Changed Type"\n\n')
            file.write('\tannotation PBI_ResultType = Table\n\n\tannotation PBI_NavigationStepName = Navigation\n\n')


class _BlobCsv(_DataSet):

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments

    '''Add a csv file store in a ADLS blob container to a dashboard

    Parameters
    ----------
    account_url: str
        The url to your Azure storage account. It should be in the format of https://<YOUR STORAGE ACCOUNT NAME>.blob.core.windows.net/. You can find it in Azure Storage Explorer by clicking on the storage account and then looking at the blob endpoint field
    blob_name: str
        The name of the blob container. In Azure Storage Explorer, click on the storage account, then inside "Blob Containers" will be all your blob containers. Use the node dislay name field.
    data_path: str
        The relative path to the file you want to load from the blob. It should be relative to blob_name
    tenant_id: str
        The tenant id of the tenant where your storage account is stored. This field is only used with browser authentication. (The default).
    use_saved_storage_key: bool
        This optional argument tells python to look in your system's default credential manager for an Azure Storage Account token and prompt the user to add one if it's not there. USE WITH CAUTION, THE STORAGE ACCOUNT TOKENS ALLOW FOR A MASSIVE AMOUNT OF ACCESS. CONSIDER USING SAS URLS OR INTERACTIVE BROWSER AUTHENTICATION INSTEAD.
    sas_url: str
        A limited time single access url scoped to just the file you want to grant read access to. To generate one from Azure Storage Explorer, right click on the file you want and then choose "Get Shared Access Signature"
    storage_account_key: str
        It is not recommended to use this when running this function on a local computer. Hardcoding credentials into code is SUPER BAD practice. Please set use_saved_storage_key to true instead. It will store the key securely in your operating system's credential manger. You should only pass a storage account key to the function if you are running this code in a cloud environment such as databricks and using that cloud platform's secure secret manager. (Something like Github Secrets or Azure Key Vault)

    Returns
    -------
    None

    Notes
    -----
    DO NOT HARD CODE CREDENTIALS. Use the use_saved_storage_key option instead.

    This function creates custom M code and is therefore more picky than pandas or Power BI desktop.
    The csv file should probably not have row numbers. (Any column without a column name will be renamed to "probably_an_index_column")
    NA values must display as "NA" or "null" not as N/A.
    If the data is malformed in Power BI, try cleaning it first in python and then rerunning this function.

    This function creates a new TMDL file defining the dataset in TMDL format and also in M code.
    The DiagramLayout and Model.tmdl files are updated to include refrences to the new dataset.
    Other dumb things: If you get an error when trying to open the .pbip file try changing the combatibility version to 1567 in the semanticmodel > definition > database.tmdl file.

    Dashboards created with the create_blank_dashboard() function start with the compatibility version set to 1567, so you should only have this problem with manually created dashboards.
    I may eventually add an automatic fix for this.

    '''

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals

    def __init__(self,
                 dashboard,
                 *,
                 data_path,
                 account_url,
                 blob_name,
                 tenant_id = None,
                 use_saved_storage_key = False,
                 sas_url = None,
                 storage_account_key = None,
                 warnings = True):

        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-locals

        super().__init__(dashboard,data_path)

        # get the account name from the url
        m = re.search("(?<=https://).*(?=\\.blob)", account_url)

        account_name = m.group(0)


        if warnings:
            if storage_account_key is not None:
                warnings.warn("DO NOT HARD CODE CREDENTIALS!! Only provide a storage_account_key argument if you're securely retreiving it from something like azure key vault. If this code is running locally set use_saved_storage_key to true instead. Set warnings = False to disable this warning. ")

        if sas_url is not None and use_saved_storage_key is True:
            raise ValueError("You can't save an azure storage key to your system's credential manager when providing an sas_url. Try changing use_saved_storage_key to False and try again")


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
                        file_path=self.data_path
                        )


            download = file_handle.download_file()
            self.dataset = pd.read_csv(download)

        elif sas_url is not None:

            print("You provided an SAS url!")
            self.dataset = pd.read_csv(sas_url)


        else:

            # retrieve the storage token
            account_token = keyring.get_password('azure_account_key', 'token')

            # if no storage token was found, prompt the user for it
            if not account_token:

                add_key = "No key has been added yet..."

                while add_key not in ("y", "n"):
                    add_key = input("Would you like to add an Azure Storage Container Key to your operating system's default credential manager?(y/n): ")

                    if add_key == "n":
                        raise ValueError("Loading files from azure requires using either an account_key, a sas_url, or an interactive browser login.\nPlease change use_saved_storage_key to 'True', allow the system to store an azure_account_key, or provide an sas_url")

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
                        file_path=self.data_path
                        )


            download = file_handle.download_file()
            self.dataset = pd.read_csv(download)

        # Build the tmdl file based on the method defined on the parent class
        self._create_tmdl()

        # write out M code
        # define tricky bits
        formatted_column_details = ', '.join(map(str, self.col_attributes["col_deets"]))

        with open(self.dataset_file_path, 'a', encoding="utf-8") as file:
            file.write(f'\tpartition {self.dataset_name} = m\n')
            file.write('\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n')
            file.write(f'\t\t\t\t\tSource = AzureStorage.Blobs("{account_url}"),\n')
            file.write(f'\t\t\t\t\t#"{blob_name}1" = Source{{[Name="{blob_name}"]}}[Data],\n')
            file.write(f'\t\t\t\t\t#"https://{account_name} blob core windows net/{blob_name}/_{data_path.replace(".csv", "")} csv" = #"{blob_name}1"{{[#"Folder Path"="{account_url}/{blob_name}/",Name="{self.data_path}"]}}[Content],\n')
            file.write(f'\t\t\t\t\t#"Imported CSV" = Csv.Document(#"https://{account_name} blob core windows net/{blob_name}/_{data_path.replace(".csv", "")} csv",[Delimiter=",", Columns={len(self.dataset.columns)}, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n')
            file.write('\t\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true]),\n')
            file.write(f'\t\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{{ formatted_column_details }}})\n')
            file.write('\t\t\t\tin\n\t\t\t\t\t#"Changed Type"\n\n')
            file.write('\tchangedProperty = Name\n\n\tannotation PBI_ResultType = Table\n\n\tannotation PBI_NavigationStepName = Navigation\n\n')
