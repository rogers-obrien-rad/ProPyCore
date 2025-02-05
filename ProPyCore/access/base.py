import urllib
import requests

from ..exceptions import raise_exception

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
            GET response in json
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
        '''
        print(f"Request URL: {response.request.url}")
        print(f"Request Headers: {response.request.headers}")
        print(f"Request Response: {response.json()}")
        '''
        
        if response.ok:
            return response.json()
        else:
            raise_exception(response)
    
    def post_request(self, api_url, additional_headers=None, params=None, data=None, files=None):
        """
        Create a HTTP Post request

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
        response : HTTP response object
            POST response details in json
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
            headers["Content-Type"] = "application/json"
            response = requests.request(
                "POST",
                url,
                headers=headers,
                json=data  # Use json parameter instead of data to properly serialize
            )
            '''
            print(f"Request URL: {response.request.url}")
            print(f"Request Headers: {response.request.headers}")
            print(f"Request Data: {response.request.body}")
            '''
        elif data is None:
            response = requests.request(
                "POST",
                url,
                headers=headers,
                files=files  # use files for multipart/form-data
            )
        else:
            response = requests.request("POST", url, headers=headers, data=data, files=files)

        if response.ok:
            return response.json()
        else:
            '''
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)
            '''
            raise_exception(response)

    def patch_request(self, api_url, additional_headers=None, params=None, data=None, files=False):
        """
        Create a HTTP PATCH request

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            PATCH parameters to parse
        data : dict, default None
            POST data to send
        files : dict or boolean, default False
            False - updating folder so use json request
            True - updating file, but no file to include
            dict - updating file with new document

        Returns
        -------
        response : HTTP response object
            PATCH response details in json
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
        
        if files is False:
            response = requests.patch(
                url,
                headers=headers,
                json=data # json for folder update
            )
        elif files is True:
            response = requests.patch(
                url,
                headers=headers,
                data=data, # data for file update
            )
        else:
            response = requests.patch(
                url,
                headers=headers,
                data=data, # data for file update
                files=files
            )

        if response.ok:
            return response.json()
        else:
            raise_exception(response)
    
    def delete_request(self, api_url, additional_headers=None, params=None):
        """
        Execute a HTTP DELETE request

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            DELETE parameters to parse

        Returns
        -------
        response : HTTP response object
            DELETE response details in json
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

        # DELETE request
        response = requests.delete(
            url=url,
            headers=headers,
        )

        if response.ok:
            return {"status_code":response.status_code}
        else:
            raise_exception(response)