from .base import Base

import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from exceptions import *

class RFI(Base):
    """
    Access and working with RFIs in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/projects"


    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Gets all the available RFIs

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        page : int, default 1
            page number
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        rfis : dict
            available rfi data
        """
        params = {
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        rfis = self.get_request(
            api_url=f"{self.endpoint}/{project_id}/rfis",
            additional_headers=headers,
            params=params
        )

        return rfis

    def show(self, company_id, project_id, rfi_id):
        """
        Shows the RFI info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        rfi_id : int
            unique identifier for the RFI

        Returns
        -------
        rfi_info : dict
            specific rfi information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        rfi_info = self.get_request(
            api_url=f"{self.endpoint}/{project_id}/rfis/{rfi_id}",
            additional_headers=headers,
        )

        return rfi_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified RFI and returns data - wrapper for show method

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for RFI which can be id (int) or number (str)

        Returns
        -------
        rfi_info : dict
            RFI data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "number"

        for rfi in self.get(company_id=company_id, project_id=project_id):
            if rfi[key] == identifier:
                rfi_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    rfi_id=rfi["id"]
                )
                return rfi_info

        raise NotFoundItemError(f"Could not find RFI {identifier}")
