import urllib
import requests

from propycore.exceptions import raise_exception

class Base:
    """
    Base class for Procore API access
    """
    
    def __init__(self, access_token, server_url) -> None:
        """
        Initializes important API access parameters

        Creates
        -------
        __access_token : str
            token to access Procore resources
        __server_url : str
            base url to send GET/POST requests
        """
        self.__access_token = access_token
        self.__server_url = server_url

    def get_request(self, api_url, params=None):
        """
        Create a HTTP Get request

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        params : dict, default None
            GET parameters to parse

        Returns
        -------
        response : dict
            GET response
        """
        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params)

        response = requests.get(url, headers={
            "Authorization": f"Bearer {self.__access_token}"
        })
        
        if response.status_code == 200:
            return response.json()
        else:
            raise_exception(response)