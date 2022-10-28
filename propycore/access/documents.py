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
            request body
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

    def remove(self, company_id, project_id, doc_id):
        """
        Deletes the give document

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
            request body
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        doc_info = self.delete_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params
        )

        return doc_info

    def list_all(self, company_id, project_id):
        """
        Lists all folders and files in the project

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        doc_info : dict
            request body
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        doc_info = self.get_request(
            api_url=f"/rest/v1.0/projects/{project_id}/documents",
            additional_headers=headers
        )

        return doc_info

class Folders(Documents):
    """
    Access to and working with Procore folders
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/folders"

    def root(self, company_id, project_id):
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

    def create(self, company_id, project_id, folder_name, parent_id=None):
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
        parent_id : int or str, default None
            the id of the parent folder to place this folder
            if not included, the folder will placed at the root

        Returns
        -------
        doc_info : dict
            request body
        """
        if parent_id is None:
            data = {
                "folder":{
                    "name": folder_name,
                    "explicit_permissions": False
                }
            }
        else:
            data = {
                "folder":{
                    "name": folder_name,
                    "parent_id": str(parent_id),
                    "explicit_permissions": False
                }
            }

        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        doc_info = self.post_request(api_url=self.endpoint, params=params, additional_headers=headers, data=data)
        
        return doc_info
        
    def update(self, company_id, project_id, doc_id, parent_id=None, folder_name=None, private=None):
        """
        Updates the given folder

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        doc_id : int
            unique identifier for the folder
        parent_id : int, default None -> root
            location where the folder exists
        folder_name : str, default None
            new name to assign to the folder
        private : boolean, default None
            permissions on the folder

        Returns
        -------
        doc_info : dict
            request body
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        # building the body from available data
        body = {}
        for key, val in zip(["parent_id","name","explicit_permissions"], [parent_id, folder_name, private]):
            if val is not None:
                body[key] = val

        data={
            "folder": body
        }

        doc_info = self.patch_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params,
            data=data
        )

        return doc_info

class Files(Documents):
    """
    Access to and working with Procore files
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/files"

    def create(self, company_id, project_id, filepath, parent_id=None, description=None):
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
        parent_id : int or str, default None
            the id of the parent folder to place this folder
            if not included, the folder will placed at the root
        description : str, default None
            optional description to include on the file

        Returns
        -------
        doc_info : dict
            request body
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        data = {
            "file[name]": f"{filepath.rsplit('/',1)[-1]}",
            "file[description]": "None" if description is None else description,
            "file[explicit_permissions]": False,
        }
        if parent_id is not None:
            data["file[parent_id]"] = int(parent_id)

        file = [
            ("file[data]", open(filepath, "rb"))
        ]

        doc_info = self.post_request(api_url=self.endpoint, additional_headers=headers, params=params, data=data, files=file)
        
        return doc_info

    def update(self, company_id, project_id, doc_id, filepath=None, parent_id=None, filename=None, description=None, private=None):
        """
        Updates the given folder

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        doc_id : int
            unique identifier for the folder
        parent_id : int, default None -> root
            location where the folder exists
        folder_name : str, default None
            new name to assign to the folder
        private : boolean, default None
            permissions on the folder

        Returns
        -------
        doc_info : dict
            request body
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        # building the body from available data
        data = {}
        for key, val in zip(["file[parent_id]","file[name]","file[description]","file[private]"], [parent_id, filename, description, private]):
            if val is not None:
                data[key] = val

        if filepath is not None:
            file = [
                ("file[data]", open(filepath, "rb"))
            ]

            doc_info = self.patch_request(
                api_url=f"{self.endpoint}/{doc_id}",
                additional_headers=headers,
                params=params,
                data=data,
                files=file
            )
        else:
            doc_info = self.patch_request(
                api_url=f"{self.endpoint}/{doc_id}",
                additional_headers=headers,
                params=params,
                data=data,
                files=True
            )

        return doc_info        