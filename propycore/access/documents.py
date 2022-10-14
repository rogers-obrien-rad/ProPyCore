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

    def create(self):
        """
        
        """
        pass

    def remove(self):
        """
        
        """
        pass

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
        
class Files(Documents):
    """
    Access to and working with Procore files
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/files"