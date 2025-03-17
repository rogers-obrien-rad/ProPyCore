from ..base import Base
from ...exceptions import NotFoundItemError, ProcoreException

class Categories(Base):
    """
    Access and working with Categories
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0"

    def get(self, company_id, project_id):
        """
        Returns a list of photo folders for a project.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        cats : list of dict
            photo category details
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        cats = []
        try:
            cats = self.get_request(
                api_url=f"{self.endpoint}/image_categories",
                params=params,
                additional_headers=headers
            )
        except ProcoreException as e:
            print(e)
        
        return cats

    def show(self, company_id, project_id, category_id):
        """
        Returns a photo folder by ID.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        category_id : int
            unique identifier for the photo folder

        Returns
        -------
        cat_info : dict
            photo folder details
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        cat_info = {}
        try:
            cat_info = self.get_request(
                api_url=f"{self.endpoint}/image_categories/{category_id}",
                params=params,
                additional_headers=headers
            )
        except ProcoreException as e:
            print(e)
        
        return cat_info

    def create(self, company_id, project_id, folder_name):
        """
        Creates a photo folder 

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
        cat_info : dict
            request body
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        cat_info = {}
        try:
            cat_info = self.post_request(
                api_url=f"{self.endpoint}/image_categories",
                params=params,
                additional_headers=headers,
                data={
                    "image_category": {
                        "name": folder_name
                    }
                }
            )
        except ProcoreException as e:
            print(e)
        
        return cat_info