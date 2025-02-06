from datetime import datetime
from ..base import Base

class Timesheets(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest" # very basic since timesheets can be at project and company levels

    def get_for_pay_period(self, company_id, page=1, per_page=100):
        """
        Return a list of all timesheet data for the given pay period
        https://developers.procore.com/reference/rest/timesheets?version=latest#list-timecard-data

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        page : int, default 1
            page number
        per_page : int, default 100
            number of timesheets to include per page

        Returns
        -------
        timesheets : list of dict
            available timesheet data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_timesheets = 1
        timesheets = []
        while n_timesheets > 0:
            params = {
                "company_id": company_id,
                "page": page,
                "per_page": per_page
            }

            timesheet_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timesheets",
                additional_headers=headers,
                params=params
            )

            n_timesheets = len(timesheet_selection)
            timesheets += timesheet_selection
            page += 1 

        return timesheets

    def get_for_specified_period(self, company_id, start_date, end_date, page=1, per_page=100, party_id=None):
        """
        Return a list of all timesheet data for the given date range (inclusive on both ends)
        https://developers.procore.com/reference/rest/timesheets?version=latest#list-timecard-data

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        start_date : datetime
            start date of pay period (inclusive)
        end_date : datetime
            end date of pay period (inclusive)
        page : int, default 1
            page number
        per_page : int, default 100
            number of timesheets to include per page
        party_id : int, default None
            procore People ID to filter by if included

        Returns
        -------
        timesheets : list of dict
            available timesheet data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_timesheets = 1
        timesheets = []
        while n_timesheets > 0:
            params = {
                "company_id": company_id,
                "page": page,
                "per_page": per_page,
                "start_date": datetime.strftime(start_date, "%Y-%m-%d"),
                "end_date": datetime.strftime(end_date, "%Y-%m-%d")
            }

            if party_id is not None:
                params["filters[party_id]"] = party_id

            timesheet_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timesheets",
                additional_headers=headers,
                params=params
            )

            n_timesheets = len(timesheet_selection)
            timesheets += timesheet_selection
            page += 1 

        return timesheets