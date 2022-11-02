from .exceptions import *
from .access import companies, projects, documents
import requests
import urllib
from bs4 import BeautifulSoup

class Procore:
    """
    Main class which creates a connection with the Procore APIs using OAuth2 (Client Credentials Grant Type).
    This grant type allows access to Procore data without having to login as a specific user. 
    """

    def __init__(self, client_id, client_secret, redirect_uri, base_url, oauth_url) -> None:
        """
        Initialize the connection

        Creates
        -------
        __client_id : str
            app's client indentifier
        __cliend_secret : str
            app's secret access token
        __redirect_uri : str
            should be "" for Client Credentials Grant Type
        __base_url : str
            the base url for RESTful
        __oauth_url : str
            authorization url to set up access
        __access_token : str
            2-hour access token to pull/push data to Procore
        """
        self.__client_id = client_id
        self.__client_secret = client_secret
        
        self.__redirect_uri = redirect_uri
        self.__base_url = base_url
        self.__oauth_url = oauth_url

        self.__access_token = None

        # get access token; resets from nothing
        self.reset_access_token()

        # create instances of useful procore endpoints
        self.__companies__ = companies.Companies(access_token=self.__access_token, server_url=self.__base_url)
        self.__projects__ = projects.Projects(access_token=self.__access_token, server_url=self.__base_url)
        self.__folders__ = documents.Folders(access_token=self.__access_token, server_url=self.__base_url)
        self.__files__ = documents.Files(access_token=self.__access_token, server_url=self.__base_url)
        
    def get_auth_code(self):
        """
        Gets the 10-minute temporary authorization token
        """
        # create url
        params = {
            "client_id": self.__client_id,
            "response_type": "code",
            "redirect_uri":  self.__redirect_uri
        }
        url = self.__oauth_url + "/oauth/authorize?" + urllib.parse.urlencode(params)
        # GET
        response = requests.get(url, headers={
            "content-type": "application/json"
        })

        auth_code = None # pre-allocate
        if response.ok:
            # use BS to parse the code from the returned html
            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup.find_all("meta"):
                if tag.get("name", None) == "csrf-token":
                    auth_code = tag.get("content", None)
        else:
            raise_exception(response=response)

        return auth_code

    def get_access_token(self, code):
        '''
        Gets access token from authorization code previously obtained from the get_auth_code call.
        
        Parameters
        ----------
        code : str
            temporary authorization code

        Returns
        -------
        <access_token> : str
            2-hour access token
        '''
        client_auth = requests.auth.HTTPBasicAuth(self.__client_id, self.__client_secret)
        post_data = {"grant_type": "client_credentials",
                    "code": code,
                    "redirect_uri": self.__redirect_uri
                    }
        response = requests.post(self.__base_url+"/oauth/token", auth=client_auth, data=post_data)
        response_json = response.json()

        return response_json["access_token"]#, response_json['created_at']

    def reset_access_token(self):
        """
        Gets a new access token
        """
        temp_code = self.get_auth_code()
        self.__access_token = self.get_access_token(temp_code)

    def find_company(self, identifier):
        """
        Finds a company based on the identifier

        Parameters
        ----------
        identifier : int or str
            company id number or name
        
        Returns
        -------
        company : dict
            company-specific dictionary
        """
        # determining which identifier to search for
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for company in self.__companies__.get():
            if company[key] == identifier:
                return company

        raise NotFoundItemError(f"Could not find company {identifier}")

    def find_project(self, company_id, identifier):
        """
        Finds a company based on the identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        identifier : int or str
            project id number or company name
        
        Returns
        -------
        project : dict
            project-specific dictionary
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for project in self.__projects__.get(company_id=company_id):
            if project[key] == identifier:
                return project

        raise NotFoundItemError(f"Could not find project {identifier}")

    def get_docs(self, company_id, project_id):
        """
        Traverses the Procore folder tree to find the given directory

        Parameters
        ----------
        connection : ProPycore connection obj
            API access to Procore
        filename : str
            name of the file with file extension
        
        Returns
        -------
        id : int
            file id
        ids : list of int
            folder ids along the way to the specified file
        """
        files_and_folders = self.__files__.list_all(company_id=company_id, project_id=project_id)
        files = []
        folders= []
        for doc in files_and_folders:
            if doc["is_deleted"] is False and doc["is_recycle_bin"] is False:
                if doc["document_type"] == "folder":
                    folders.append(doc)
                else:
                    files.append(doc)

        return files, folders

    def find_doc(self, company_id, project_id, name, look_for_file=False):
        """
        Finds the information from the folder name

        Parameters
        ----------
        company : int or str
            company id number or name
        project : : int or str
            project id number or name
        name : str
            name of the file or folder to look for
        look_for_file : boolean, default False
            whether to look for file or folder

        Returns
        -------
        doc : dict
            doc-specific dictionary
        """
        files, folders = self.get_docs(company_id=company_id, project_id=project_id)
        if look_for_file:
            docs = files
        else:
            docs = folders

        for doc in docs:
            if doc["name"] == name:
                return doc

        raise NotFoundItemError(f"Could not find document {name}")
