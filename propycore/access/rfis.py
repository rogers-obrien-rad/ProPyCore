from .base import Base

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

    