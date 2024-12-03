from ..base import Base
from ...exceptions import NotFoundItemError, ProcoreException, WrongParamsError

from warnings import warn
from fuzzywuzzy import fuzz

class Folders(Base):
    """
    Access to and working with Procore folders
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/folders"

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

    def get(self, company_id, project_id, folder_id=None):
        """
        Gets all documents in a project

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        docs : list of dict
            available docs and their corresponding response body
        """
        # get document type (file or folder) from endpoint
        doc_type = self.endpoint.split("/")[-1][:-1] # remove last char which is an "s"

        n_docs = 1
        page = 1
        docs = []
        while n_docs > 0:

            params = {
                "view": "normal",
                "sort": "name",
                "page": page,
                "per_page": 10000,
                "filters[document_type]": doc_type,
                "filters[is_in_recycle_bin]": False
            }
            if folder_id is not None:
                params["filters[folder_id]"] = folder_id

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            doc_info = self.get_request(
                api_url=f"/rest/v1.0/projects/{project_id}/documents",
                additional_headers=headers,
                params=params
            )

            n_docs = len(doc_info)

            for doc in doc_info:
                if doc["is_deleted"] is False:
                    docs.append(doc)

            page += 1 

        if len(docs) > 0:
            return docs
        else:
            raise NotFoundItemError(f"No {doc_type}s are available in Project {project_id} from Parent ID {folder_id if folder_id is not None else 'Root'}")

    def search(self, company_id, project_id, value, folder_id=None):
        """
        Searches through all available files to find the closet match to the given value.
        For documents with the same match score, the last document to be found is returned.
        Folders in root are searched completely first (in alphanumeric order) and then files
        in the root are considered. 

        Parameters
        ----------
        company : int or str
            company id number or name
        project : : int or str
            project id number or name
        value : str
            search criteria
        folder_id : int, default None
            id of parent folder

        Returns
        -------
        result : dict
            document reference information
        """
        docs = self.get(
            company_id=company_id,
            project_id=project_id,
            folder_id=folder_id
        )

        # get document type (file or folder) from endpoint
        doc_type = self.endpoint.split("/")[-1][:-1] # remove last char which is an "s"

        # dummy values for finding best match
        score = 0
        n_perfect = 0
        result = {}
        for doc in docs:
            # filter for only active documents
            if not doc["is_deleted"] and not doc["is_recycle_bin"] and doc["document_type"] == doc_type:
                temp_score = fuzz.partial_ratio(value, doc["name"])
                if temp_score == 100:
                    n_perfect += 1
                # update match values
                if temp_score >= score:
                    score = temp_score
                    result = doc

        # warn if multiple documents provided perfect match
        if n_perfect > 1:
            warn("Multiple 100% matches - try refining your search critera for better results")

        # raise an error if the document can't be found
        if score == 0:
            raise NotFoundItemError(f"Could not find document {value}")
        else:
            result["search_criteria"] = {"value":value, "match":score}
            return result

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

    def create(self, company_id, project_id, folder_name, folder_id=None):
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
        folder_id : int or str, default None
            the id of the parent folder to place this folder
            if not included, the folder will placed at the root

        Returns
        -------
        doc_info : dict
            request body
        """
        if folder_id is None:
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
                    "parent_id": str(folder_id),
                    "explicit_permissions": False
                }
            }

        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            doc_info = self.post_request(
                api_url=self.endpoint,
                params=params,
                additional_headers=headers,
                data=data
            )
        except ProcoreException as e:
            print(e)
        
        return doc_info
        
    def update(self, company_id, project_id, doc_id, folder_id=None, folder_name=None, private=None):
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
        folder_id : int, default None -> root
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
        for key, val in zip(["parent_id","name","explicit_permissions"], [folder_id, folder_name, private]):
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
    
    def find(self, company_id, project_id, identifier, folder_id=None):
        """
        Finds the information from the folder name

        Parameters
        ----------
        company : int or str
            company id number or name
        project : : int or str
            project id number or name
        identifier : str
            name of the folder to look for
        folder_id : int, default None
            parent id to get subfolder in
            None specifies to start at the root

        Returns
        -------
        <folder_info> : dict
            folder-specific dictionary
        """
        folders = self.get(
            company_id=company_id,
            project_id=project_id,
            folder_id=folder_id
        )

        for folder in folders:
            if folder["name"] == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    doc_id=folder["id"]
                )

        raise NotFoundItemError(f"Could not find document {identifier}")