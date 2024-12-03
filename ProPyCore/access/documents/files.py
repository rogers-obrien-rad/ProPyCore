from ..base import Base
from ...exceptions import NotFoundItemError, ProcoreException, WrongParamsError
from warnings import warn
from fuzzywuzzy import fuzz


class Files(Base):
    """
    Access to and working with Procore files.
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/files"

    def create(self, company_id, project_id, filepath, folder_id=None, description=None):
        """
        Creates a file.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        filepath : str
            Path to the file to upload.
        folder_id : int or str, default None
            The ID of the parent folder to place this folder.
            If not included, the folder will be placed at the root.
        description : str, default None
            Optional description to include on the file.

        Returns
        -------
        doc_info : dict
            Request body.
        """
        params = {"project_id": project_id}

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        filename = filepath.rsplit('/', 1)[-1]
        data = {
            "file[name]": f"{filename}",
            "file[description]": "None" if description is None else description,
        }

        if folder_id is not None:
            data["file[parent_id]"] = int(folder_id)

        file = [("file[data]", open(filepath, "rb"))]

        try:
            doc_info = self.post_request(
                api_url=self.endpoint,
                additional_headers=headers,
                params=params,
                data=data,
                files=file,
            )
        except ProcoreException as e:
            print(e)

        return doc_info

    def update(self, company_id,project_id,doc_id,filepath=None,folder_id=None,filename=None,description=None,private=None):
        """
        Updates the given folder.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        doc_id : int
            Unique identifier for the folder.
        folder_id : int, default None -> root
            Location where the folder exists.
        folder_name : str, default None
            New name to assign to the folder.
        private : boolean, default None
            Permissions on the folder.

        Returns
        -------
        doc_info : dict
            Request body.
        """
        params = {"project_id": project_id}

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        data = {}
        keys = ["file[parent_id]", "file[name]", "file[description]", "file[private]"]
        values = [folder_id, filename, description, private]
        for key, val in zip(keys, values):
            if val is not None:
                data[key] = val

        if filepath is not None:
            file = [("file[data]", open(filepath, "rb"))]

            doc_info = self.patch_request(
                api_url=f"{self.endpoint}/{doc_id}",
                additional_headers=headers,
                params=params,
                data=data,
                files=file,
            )
        else:
            doc_info = self.patch_request(
                api_url=f"{self.endpoint}/{doc_id}",
                additional_headers=headers,
                params=params,
                data=data,
                files=True,
            )

        return doc_info

    def find(self, company_id, project_id, identifier, folder_id=None):
        """
        Finds the information from the folder name.

        Parameters
        ----------
        company : int or str
            Company ID number or name.
        project : : int or str
            Project ID number or name.
        identifier : str
            Name of the file or folder to look for.
        folder_id : int, default None
            Parent ID to get subfolder in.
            None specifies to start at the root.

        Returns
        -------
        doc : dict
            Doc-specific dictionary.
        """
        files = self.get(
            company_id=company_id,
            project_id=project_id,
            folder_id=folder_id,
        )

        for file in files:
            if file["name"] == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    doc_id=file["id"],
                )

        raise NotFoundItemError(f"Could not find document {identifier}")

    def show(self, company_id, project_id, doc_id):
        """
        Show information regarding the given folder or file.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        doc_id : int
            Unique identifier for the folder or file.

        Returns
        -------
        doc_info : dict
            Request body.
        """
        params = {"project_id": project_id}

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        doc_info = self.get_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params,
        )

        return doc_info

    def remove(self, company_id, project_id, doc_id):
        """
        Deletes the given document.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        doc_id : int
            Unique identifier for the folder or file.

        Returns
        -------
        doc_info : dict
            Request body.
        """
        params = {"project_id": project_id}

        headers = {
            "Procore-Company-Id": f"{company_id}",
        }

        doc_info = self.delete_request(
            api_url=f"{self.endpoint}/{doc_id}",
            additional_headers=headers,
            params=params,
        )

        return doc_info

    def get(self, company_id, project_id, folder_id=None):
        """
        Gets all documents in a project.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.

        Returns
        -------
        docs : list of dict
            Available docs and their corresponding response body.
        """
        doc_type = self.endpoint.split("/")[-1][:-1]

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
                "filters[is_in_recycle_bin]": False,
            }
            if folder_id is not None:
                params["filters[folder_id]"] = folder_id

            headers = {
                "Procore-Company-Id": f"{company_id}",
            }

            doc_info = self.get_request(
                api_url=f"/rest/v1.0/projects/{project_id}/documents",
                additional_headers=headers,
                params=params,
            )

            n_docs = len(doc_info)

            for doc in doc_info:
                if doc["is_deleted"] is False:
                    docs.append(doc)

            page += 1

        if len(docs) > 0:
            return docs
        else:
            raise NotFoundItemError(
                f"No {doc_type}s are available in Project {project_id} "
                f"from Parent ID {folder_id if folder_id is not None else 'Root'}",
            )

    def search(self, company_id, project_id, value, folder_id=None):
        """
        Searches through all available files to find the closest match to the given value.

        Parameters
        ----------
        company : int or str
            Company ID number or name.
        project : : int or str
            Project ID number or name.
        value : str
            Search criteria.
        folder_id : int, default None
            ID of parent folder.

        Returns
        -------
        result : dict
            Document reference information.
        """
        docs = self.get(
            company_id=company_id,
            project_id=project_id,
            folder_id=folder_id,
        )

        doc_type = self.endpoint.split("/")[-1][:-1]

        score = 0
        n_perfect = 0
        result = {}
        for doc in docs:
            if not doc["is_deleted"] and not doc["is_recycle_bin"] and doc["document_type"] == doc_type:
                temp_score = fuzz.partial_ratio(value, doc["name"])
                if temp_score == 100:
                    n_perfect += 1
                if temp_score >= score:
                    score = temp_score
                    result = doc

        if n_perfect > 1:
            warn("Multiple 100% matches - try refining your search criteria for better results")

        if score == 0:
            raise NotFoundItemError(f"Could not find document {value}")
        else:
            result["search_criteria"] = {"value": value, "match": score}
            return result
