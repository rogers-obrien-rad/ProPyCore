    
from ..base import Base
from ...exceptions import NotFoundItemError

class Timecards(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest" # very basic since timecards can be at project and company levels

    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Returns a list of all timecard data for a given project: https://developers.procore.com/reference/rest/timecard-entries?version=latest
        
        Parameters
        ----------
        company_id : int
            unique identifier for the company
        prject_id : int
            unique identifier for the project
        page : int, default 1
            page number
        per_page : int, default 100
            number of rfis to include per page

        Returns
        -------
        timecards : list of dict
            available timecard data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_timecards = 1
        timecards = []
        while n_timecards > 0:
            params = {
                "project_id": project_id,
                "page": page,
                "per_page": per_page
            }

            timecard_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.0/projects/{project_id}/timecard_entries",
                additional_headers=headers,
                params=params
            )

            n_timecards = len(timecard_selection)
            timecards += timecard_selection
            page += 1 

        return timecards

    def get_timecards_for_pay_period(self, company_id, page=1, per_page=100):
        """
        Return a list of all timecard data for the given pay period: https://developers.procore.com/reference/rest/timesheets?version=latest#list-timecard-data

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        page : int, default 1
            page number
        per_page : int, default 100
            number of rfis to include per page

        Returns
        -------
        timecards : list of dict
            available timecard data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_timecards = 1
        timecards = []
        while n_timecards > 0:
            params = {
                "company_id": company_id,
                "page": page,
                "per_page": per_page
            }

            timecard_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timesheets",
                additional_headers=headers,
                params=params
            )

            n_timecards = len(timecard_selection)
            timecards += timecard_selection
            page += 1 

        return timecards