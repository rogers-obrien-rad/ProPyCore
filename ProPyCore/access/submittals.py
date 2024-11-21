import asyncio
from .base import Base
from ..exceptions import *

class Submittal(Base):
    """
    Access and working with submittals in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.1/projects"

    def get(self, company_id, project_id):
        """
        Synchronous wrapper for the async_get method.
        """
        return asyncio.run(self.async_get(company_id, project_id))

    async def async_get(self, company_id, project_id):
        """
        Asynchronous implementation of fetching all available Submittals.

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
        headers = {"Procore-Company-Id": f"{company_id}"}
        api_url = f"{self.endpoint}/{project_id}/submittals"

        async def fetch_page(page):
            params = {"page": page, "per_page": 100}
            return await self.get_request_async(api_url, additional_headers=headers, params=params)

        # Create tasks for multiple pages
        tasks = [fetch_page(page) for page in range(1, 101)]  # Adjust range as needed
        results = await asyncio.gather(*tasks)

        # Flatten results
        submittals = [item for sublist in results for item in sublist if sublist]
        return submittals

    def show(self, company_id, project_id, submittal_id):
        """
        Shows the Submittal info.

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
        headers = {"Procore-Company-Id": f"{company_id}"}
        submittal_info = self.get_request(
            api_url=f"{self.endpoint}/{project_id}/submittals/{submittal_id}",
            additional_headers=headers,
        )
        return submittal_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified submittal.

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
        submittals = self.get(company_id=company_id, project_id=project_id)
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for submittal in submittals:
            if submittal[key] == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    submittal_id=submittal["id"]
                )

        raise NotFoundItemError(f"Could not find Submittal {identifier}")