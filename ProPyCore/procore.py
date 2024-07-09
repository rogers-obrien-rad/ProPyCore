from .exceptions import *
from .access import companies, generic_tools, projects, documents, rfis, directory, submittals, tasks, budgets
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

        # create instances of procore endpoints
        self.__companies__ = companies.Companies(access_token=self.__access_token, server_url=self.__base_url)
        self.__projects__ = projects.Projects(access_token=self.__access_token, server_url=self.__base_url)

        self.__folders__ = documents.Folders(access_token=self.__access_token, server_url=self.__base_url)
        self.__files__ = documents.Files(access_token=self.__access_token, server_url=self.__base_url)

        self.__rfis__ = rfis.RFI(access_token=self.__access_token, server_url=self.__base_url)
        self.__submittals__ = submittals.Submittal(access_token=self.__access_token, server_url=self.__base_url)
        self.__tasks__ = tasks.Task(access_token=self.__access_token, server_url=self.__base_url)
        self.__tools__ = generic_tools.GenericTool(access_token=self.__access_token, server_url=self.__base_url)

        self.__users__ = directory.Users(access_token=self.__access_token, server_url=self.__base_url)
        self.__vendors__ = directory.Vendors(access_token=self.__access_token, server_url=self.__base_url)
        self.__trades__ = directory.Trades(access_token=self.__access_token, server_url=self.__base_url)

        self.__budgets__ = budgets.Budgets(access_token=self.__access_token, server_url=self.__base_url)
        
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
