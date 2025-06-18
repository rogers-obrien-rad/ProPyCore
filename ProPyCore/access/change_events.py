from .base import Base
from ..exceptions import *

class ChangeEvent(Base):
    """
    Access and working with change events in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0"

    def get_statuses(self, company_id, project_id):
        """
        Gets all the available change event statuses

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        change_event_statuses : dict
            available change event statuses
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        params = {
            "project_id": project_id
        }
        return self.get_request(
            api_url=f"{self.endpoint}/change_event/statuses",
            additional_headers=headers,
            params=params
        )

    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Gets all the available change events

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
        change_events : dict
            available change events data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        n_events = 1
        page = 1
        events = []
        while n_events > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "project_id": project_id
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            event_selection = self.get_request(
                api_url=f"{self.endpoint}/change_events",
                additional_headers=headers,
                params=params
            )

            n_events = len(event_selection)
            events += event_selection
            page += 1 

        return events

    def show(self, company_id, project_id, event_id):
        """
        Shows the Change Event info.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        event_id : int
            unique identifier for the event

        Returns
        -------
        event_info : dict
            specific event information
        """
        headers = {"Procore-Company-Id": f"{company_id}"}
        params = {"project_id": project_id}
        event_info = self.get_request(
            api_url=f"{self.endpoint}/change_events/{event_id}",
            additional_headers=headers,
            params=params
        )
        return event_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified change event.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for Change Event

        Returns
        -------
        event_info : dict
            event data
        """
        events = self.get(company_id=company_id, project_id=project_id)
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for event in events:
            if event[key] == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    event_id=event["id"]
                )

        raise NotFoundItemError(f"Could not find Change Event {identifier}")