from .base import Base

class Documents(Base):
    """
    Wrapper class for Folders and Files - should NOT instantiate directly
    Basic functionality for working with Folders and Files
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = None # create dummy endpoint so the methods have a reference

    def show(self, company_id, project_id, doc_id):
        """
        Show information regarding the given folder or file

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        doc_id : int
            unique identifier for the folder or file

        Returns
        -------
        doc_info : dict

        """
        
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        doc_info = self.get_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params
        )

        return doc_info

    def update(self):
        """
        
        """
        pass

    def remove(self, company_id, project_id, doc_id):
        """
        
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        response = self.delete_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params
        )

        if response.ok:
            return f"{response.status_code}: Successfully deleted document {doc_id}"
        else:
            return f"{response.status_code}: Could not delete document {doc_id}"

class Folders(Documents):
    """
    Access to and working with Procore folders
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/folders"

    def get(self, company_id, project_id):
        """
        Gets the list of root folders and files

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        docs : dict
            json-like information on root folders and files
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}" # needs to be a str
        }

        docs = self.get_request(
            api_url=self.endpoint,
            additional_headers=headers,
            params=params
        )

        return docs

    def create(self, company_id, project_id, folder_name):
        """
        Creates a folder 

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        folder_name : str
            name of the folder to create

        Returns
        -------
        <status_message> : str
            success/error message
        """
        data = {
            "folder":{
                "name": folder_name,
            }
        }

        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        response = self.post_request(api_url=self.endpoint, params=params, additional_headers=headers, data=data)
        if response.ok:
            return f"{response.status_code}: succesfully created {folder_name}"
        elif response.status_code == 400:
            return f"{response.status_code}: {folder_name} already exists and cannot be overwritten"
        else:
            return f"{response.status_code}: failed to create {folder_name}"
        
class Files(Documents):
    """
    Access to and working with Procore files
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/files"

    def create(self, company_id, project_id, filepath):
        """
        Creates a file 

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        filepath : str
            path to the file to upload
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        data = {
            "file[name]": f"{filepath.rsplit('/',1)[-1]}",
        }

        file = [
            ("file[data]", open(filepath, "rb"))
        ]

        response = self.post_request(api_url=self.endpoint, additional_headers=headers, params=params, data=data, files=file)
        if response.ok:
            return f"{response.status_code}: succesfully created {data['file[name]']}"
        elif response.status_code == 400:
            return f"{response.status_code}: {data['file[name]']} already exists and cannot be overwritten"
        else:
            return f"{response.status_code}: failed to create {data['file[name]']}"

        