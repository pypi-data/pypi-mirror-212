from daspython.auth.authenticate import DasAuth
from daspython.services.alcs.aclservice import AclService
from daspython.services.attributes.attributeservice import AttributeService
from daspython.services.digitalobjects.digitalobjectservice import DigitalObjectService
from daspython.services.entries.entryservice import EntryService, GetAllEntriesRequest, InsertRequest, UpdateRequest
from daspython.common.api import Token
from daspython.services.entryfields.entryfieldservice import DisplayType, EntryFieldService
from daspython.services.searches.searchservice import SearchEntriesRequest, SearchService

class DasClient():

    __token: Token

    def __init__(self, username:str, password:str, base_url:str, check_https:bool=True):
        auth = DasAuth(base_url, username, password)
        auth.authenticate(check_https)
        self.__token = auth


    def get_attribute_name(self, attribute_id:int):
        """
        Gets the name of an attribute by its id

        Parameters
        ----------
        attribute_id : int
            The id of the attribute to get the name from
        """

        service = AttributeService(self.__token)
        return service.get_attribute_name(attribute_id) 

    def get_attribute_id(self, attribute_name:str):
        """
        Gets the id of an attribute by its name

        Parameters
        ----------
        attribute_name : str
            The name of the attribute to get the id from
        """

        service = AttributeService(self.__token)
        return service.get_attribute_id(attribute_name)           

    def get_entries(self, attribute_name, page = 0, max_results_per_page = 10, sort = "displayname asc", filter = ""):

        service = EntryService(self.__token)
        request = GetAllEntriesRequest()

        attribute_service = AttributeService(self.__token)
        attribute_id = attribute_service.get_attribute_id(attribute_name)

        request.skipcount = page
        request.maxresultcount = max_results_per_page
        request.sorting = sort
        request.querystring = filter
        request.attributeid = attribute_id        

        return service.get_all(request)
    
    def get_by_code(self, entry_code):
            """
            Gets the entry by its code

            Parameters
            ----------
            entry_code : str
                The entry code of the entry to get
            """

            service = EntryService(self.__token)
            return service.get_entry_by_code(entry_code)
    
    def create_entries_from_excel(self, attribute_name, entries):
        """
        Inserts entries from an excel file. Example of usage:

        .. code-block:: python

        import pandas as pd

        
        df = pd.read_excel('C:\\Workspace\\das-python\\core_test_template.xlsx')
        entries = df.to_dict('records')
        das.create_entries_from_excel('cores', entries)                   

        Parameters
        ----------
        attribute_name : str
            The name of the attribute to insert the entries to
        entries : list
            A list of entries to insert
        """                        

        service = service = EntryService(self.__token)
        request = InsertRequest()

        attribute_service = AttributeService(self.__token)
        attribute_id = attribute_service.get_attribute_id(attribute_name)        
        request.attributeId = attribute_id
        service.insert_from_excel(attribute_id, entries)

    def create_entry(self, attribute_name, entry):
        service = EntryService(self.__token)
        attribute_service = AttributeService(self.__token)
        request = InsertRequest()
        attribute_id = attribute_service.get_attribute_id(attribute_name)        
        request.attributeId = attribute_id
        request.entry = entry
        new_entry_id = service.insert(request)
        return new_entry_id        
    
    def delete_entry(self, entry_code) -> bool:
        """
        Deletes an entry by its code

        Parameters
        ----------
        entry_code : str
            The entry code of the entry to delete
        """
        service = EntryService(self.__token)        
        response = service.get_entry_by_code(entry_code)
        if response is None:
            return False        
        return service.delete_entry(id=response.entry.get('id'), attributeId=response.attributeId)         
    
    def download_template(self, attriubte_name, file_path):
        """
        Downloads the template for an attribute

        Parameters
        ----------
        attriubte_name : str
            The name of the attribute to download the template from
        file_path : str
            The path to save the template to
        """

        service = AttributeService(self.__token)
        attribute_service = AttributeService(self.__token)
        attribute_id = attribute_service.get_attribute_id(attriubte_name)
        service.get_file_template(attribute_id, 1, file_path)

    def change_owner(self, entry_code, user_email) -> bool:
        """
        Changes the ownership of an entry to the current user

        Parameters
        ----------
        entry_code : str
            The entry code of the entry to change ownership
        user_email : str 
            The email of the user to change ownership to            
        """        
        acl_service = AclService(self.__token)
        return acl_service.change_owner_v2(code=entry_code, new_owner_email=user_email)
    
    def update_entry(self, code, entry) -> bool:
        """
        Updates an entry by its code

        Parameters
        ----------
        code : str
            The entry code of the entry to update
        entry : dict
            The entry to update
        """
        service = EntryService(self.__token)        
        response = service.get_entry_by_code(code)
        if response is None:
            return False
        
        edit_request = UpdateRequest()
        edit_request.attributeId = response.attributeId
        edit_request.entry = entry
        entry['id'] = response.entry['id']
        return service.edit(edit_request) not in [None, False]       

    def upload_digital_object(self, code, file_path, description):
        """
        Uploads a digital object to an entry

        Parameters
        ----------
        code : str
            The entry code of the entry to upload the digital object to
        file_path : str
            The path of the file to upload
        """
        digital_object_service = DigitalObjectService(self.__token)        
        digital_object_service.upload_to_entry(code, file_path, description)

    def link_digital_object(self, entry_code, digital_object_code):
        """
        Links a digital object to an entry

        Parameters
        ----------
        entry_code : str
            The entry code of the entry to link the digital object to
        digital_object_code : str
            The code of the digital object to link
        """
        digital_object_service = DigitalObjectService(self.__token)  
        digital_object_service.link_existing(entry_code, digital_object_code)   

    def request_digital_objects(self, entry_code, digital_object_codes: list[str] = []):
        """
        Requests a digital object

        Parameters
        ----------
        entry_code : str
            The entry code of the entry to request the digital object from      

        digital_object_codes : list[str]
            The codes of the digital objects to request
        """
        digital_object_service = DigitalObjectService(self.__token)
        digital_object_service.download_request(entry_code, digital_object_codes)

    def get_my_download_requests_info(self):
        """
        Gets the download requests for the current user
        """
        digital_object_service = DigitalObjectService(self.__token)
        response = digital_object_service.get_my_requests()    
        return response
    
    def get_files_from_download_request(self):
        """
        Gets the files from the download request
        """
        digital_object_service = DigitalObjectService(self.__token)
        digital_object_service.get_files_from_download_request() 

    def search(self, attribute_name, query="", page=1, max_results_per_page=10, sort=""):
        f"""
        Searches for entries

        Parameters
        ----------
        attribute_name : str
            The name of the attribute to search
        query : str
            The query to search (e.g. "name(entry name);code(entry code)")
        page : int  
            The page number to search (default is 1)
        max_results_per_page : int (default is 10)
            The maximum number of results per page
        sort : str (name DESC OR name ASC)
            The sort order
        """
        
        # Coverts display name columns to column names

        attribute_service = AttributeService(self.__token)
        attribute_id = attribute_service.get_attribute_id(attribute_name)

        entry_filed_service = EntryFieldService(self.__token)
        entry_fields_response = entry_filed_service.get_all(attribute_id, displayType=DisplayType.FORM)
        entry_fields = entry_fields_response.items

        for entry_field in entry_fields:            
                query = query.replace(entry_field.get('displayName'), entry_field.get('column'))
                sort = sort.replace(entry_field.get('displayName'), entry_field.get('column'))

        search = SearchService(self.__token)

        request = SearchEntriesRequest()           
        request.maxresultcount = max_results_per_page
        request.querystring = query
        request.sorting = sort
        request.attributeId = attribute_id

        if (page >= 1):
            request.skipcount = (page - 1) * max_results_per_page

        response = search.search_entries(request)

        return response
        
        
