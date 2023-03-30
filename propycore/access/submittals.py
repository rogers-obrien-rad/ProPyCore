from .base import Base

import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from exceptions import *

import pandas as pd
from datetime import datetime

class Submittal(Base):
    """
    Access and working with submittals in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1/projects"


    def get(self, company_id, project_id):
        """
        Gets all the available Submittals

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        submittals : dict
            available submittal data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_submittals = 1
        page = 1
        submittals = []
        while n_submittals > 0:

            params = {
                "page": page,
                "per_page": 100
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            submittal_selection = self.get_request(
                api_url=f"{self.endpoint}/{project_id}/submittals",
                additional_headers=headers,
                params=params
            )

            n_submittals = len(submittal_selection)
            submittals += submittal_selection
            page += 1 

        return submittals

    def show(self, company_id, project_id, submittal_id):
        """
        Shows the Submittal info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        submittal_id : int
            unique identifier for the submittal

        Returns
        -------
        submittal_info : dict
            specific submittal information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        submittal_info = self.get_request(
            api_url=f"{self.endpoint}/{project_id}/submittals/{submittal_id}",
            additional_headers=headers,
        )

        return submittal_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified submittal

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for Submittal

        Returns
        -------
        submittal_info : dict
            submittal data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for submittal in self.get(company_id=company_id, project_id=project_id):
            if submittal[key] == identifier:
                submittal_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    submittal_id=submittal["id"]
                )
                return submittal_info

        raise NotFoundItemError(f"Could not find Submittal {identifier}")