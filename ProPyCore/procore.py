from .exceptions import *
from .access import companies, generic_tools, projects, documents, rfis, directory, submittals, tasks, budgets, direct_costs, cost_codes, time, quality, photos
import requests

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
        # General
        self.companies = companies.Companies(access_token=self.__access_token, server_url=self.__base_url)
        self.projects = projects.Projects(access_token=self.__access_token, server_url=self.__base_url)
        # Documents
        self.folders = documents.Folders(access_token=self.__access_token, server_url=self.__base_url)
        self.files = documents.Files(access_token=self.__access_token, server_url=self.__base_url)
        self.photos = photos.Photos(access_token=self.__access_token, server_url=self.__base_url)
        # Tools
        self.rfis = rfis.RFI(access_token=self.__access_token, server_url=self.__base_url)
        self.submittals = submittals.Submittal(access_token=self.__access_token, server_url=self.__base_url)
        self.tasks = tasks.Task(access_token=self.__access_token, server_url=self.__base_url)
        self.tools = generic_tools.GenericTool(access_token=self.__access_token, server_url=self.__base_url)
        # People
        self.directory = directory.Directory(access_token=self.__access_token, server_url=self.__base_url)
        # Financials
        self.budgets = budgets.Budgets(access_token=self.__access_token, server_url=self.__base_url)
        self.direct_costs = direct_costs.DirectCosts(access_token=self.__access_token, server_url=self.__base_url)
        self.cost_codes = cost_codes.CostCodes(access_token=self.__access_token, server_url=self.__base_url)
        # Time
        self.time = time.Time(access_token=self.__access_token, server_url=self.__base_url)
        # Quality
        self.quality = quality.Quality(access_token=self.__access_token, server_url=self.__base_url)

    def get_access_token(self):
        """
        Gets access token from authorization code previously obtained from the get_auth_code call.
        
        Parameters
        ----------
        code : str
            temporary authorization code

        Returns
        -------
        <access_token> : str
            2-hour access token
        """
        client_auth = requests.auth.HTTPBasicAuth(self.__client_id, self.__client_secret)
        post_data = {
            "grant_type": "client_credentials",
            "redirect_uri": self.__redirect_uri
        }
        response = requests.post(self.__base_url+"/oauth/token", auth=client_auth, data=post_data)
        response_json = response.json()

        return response_json["access_token"]

    def reset_access_token(self):
        """
        Gets a new access token
        """
        self.__access_token = self.get_access_token()

    def print_attributes(self):
        """
        Print all attributes of the Procore object
        """
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")
