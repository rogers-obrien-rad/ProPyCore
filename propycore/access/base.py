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

    def get_request(self, api_url, additional_headers=None, params=None):
        """
        Create a HTTP Get request

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
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

        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise_exception(response)

    def post_request(self, api_url, additional_headers=None, params=None, data=None, files=None):
        """
        Create a HTTP Get request

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        data : dict, default None
            POST data to send
        files : list of tuple, default None
            open files to send to Procore

        Returns
        -------
        response : dict
            GET response
        """
        # Get URL
        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params)

        # Get Headers
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        # Make the request with file if necessary
        if files is None:
            response = requests.post(
                url,
                headers=headers,
                json=data
            )
        else:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                files=files
            )
        
        return response