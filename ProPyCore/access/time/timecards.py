from datetime import datetime
from ..base import Base
from ..directory.people import People
from ..cost_codes import CostCodes

class Timecards(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest" # very basic since timecards can be at project and company levels
        self.people = People(access_token, server_url)
        self.cost_codes = CostCodes(access_token, server_url)

    def get_time_types(self, company_id):
        """
        Gets the time types at the company level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        
        Returns
        -------
        <time_types> : list of dict
            list where each value is a dict with a time type's information
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        return self.get_request(
            api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timecard_time_types",
            additional_headers=headers
        )
        
    def find_time_type(self, company_id, time_type_identifier):
        """
        Finds a specific time type at the company level.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        time_type_identifier : str or int
            Unique identifier for the time type.
            If integer, match 'id' field.
            If string, match 'name' field.
        
        Returns
        -------
        matched : dict
            The time type information if found, otherwise None.
        """
        try:
            # Fetch all time types for the company
            time_types = self.get_time_types(company_id)

            # Determine if identifier is int or str
            if isinstance(time_type_identifier, int):
                # Match by 'id' field
                matched = next((tt for tt in time_types if tt['id'] == time_type_identifier), None)
            elif isinstance(time_type_identifier, str):
                # Match by 'name' field (case-insensitive)
                matched = next((tt for tt in time_types if tt['name'].lower() == time_type_identifier.lower()), None)
            else:
                raise ValueError("time_type_identifier must be either an integer (id) or a string (name).")

            return matched
        except Exception as e:
            print(f"Error finding time type: {e}")
            return None
    
    def get_for_day(self, company_id, project_id, entry_date=None, page=1, per_page=100):
        """
        Returns a list of all daily timecard data for a given project
        https://developers.procore.com/reference/rest/timecard-entries?version=latest
        
        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        entry_date : datetime, default None
            date to pull timecards
            None specifies current day
        page : int, default 1
            page number
        per_page : int, default 100
            number of timecards to include per page

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
            if entry_date is None:
                params = {
                    "project_id": project_id,
                    "page": page,
                    "per_page": per_page
                }
            else:
                params = {
                    "project_id": project_id,
                    "page": page,
                    "per_page": per_page,
                    "log_date": datetime.strftime(entry_date, "%Y-%m-%d")
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

    def get_for_specified_period(self, company_id, start_date, end_date, page=1, per_page=100, party_id=None):
        """
        Return a list of all timecard data for the given date range (inclusive on both ends)
        https://developers.procore.com/reference/rest/timecard-entries?version=latest#list-timecard-entries-company

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
            number of timecards to include per page
        party_id : int, default None
            procore People ID to filter by if included

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
                "per_page": per_page,
                "start_date": datetime.strftime(start_date, "%Y-%m-%d"),
                "end_date": datetime.strftime(end_date, "%Y-%m-%d")
            }

            if party_id is not None:
                params["filters[party_id]"] = party_id

            timecard_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timecard_entries",
                additional_headers=headers,
                params=params
            )

            n_timecards = len(timecard_selection)
            timecards += timecard_selection
            page += 1 

        return timecards

    def create(self, company_id, project_id, data):
        """
        Create a new timecard in a given a project.
        https://developers.procore.com/reference/rest/timecard-entries?version=latest#create-timecard-entry-project

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Procore's unique identifier for the project.
        data : dict
            Timecard data to create.
        """
        # Check and handle 'hours'
        if "hours" in data:
            data["hours"] = str(data["hours"])  # Convert to str to ensure Procore accepts it
        else:
            raise ValueError("Input data must have an 'hours' field.")

        # Check party ID (person's ID)
        if "party_id" in data:
            if isinstance(data["party_id"], int):
                # Assume it is valid person ID
                pass
            else:
                # send party id to people.find() to resolve - it will take care of name vs email field based on the value
                person = self.people.find(company_id, data["party_id"])
                data["party_id"] = int(person["id"])
        else:
            pass
            raise ValueError("Input data must have a 'party_id' field.")

        # Check and handle 'timecard_time_type_id'
        if "timecard_time_type_id" not in data:
            # Default to 'Salary' time type
            salary_time_type = self.find_time_type(company_id, "Salary")
            if not salary_time_type:
                raise ValueError("Could not find the 'Salary' time type.")
            data["timecard_time_type_id"] = int(salary_time_type["id"])
        else:
            time_type_id = data["timecard_time_type_id"]

            if isinstance(time_type_id, int):
                # If int, assume it's valid
                pass
            elif isinstance(time_type_id, str):
                # If str, use find_time_type to resolve
                resolved_time_type = self.find_time_type(company_id, time_type_id)
                if not resolved_time_type:
                    raise ValueError(f"Time type '{time_type_id}' not found.")
                data["timecard_time_type_id"] = int(resolved_time_type["id"])
            else:
                raise ValueError("'timecard_time_type_id' must be an integer or string.")

        # Check and handle cost code and line item type IDs
        need_cost_code = "cost_code_id" not in data or not isinstance(data["cost_code_id"], int)
        need_line_item = "line_item_type_id" not in data or not isinstance(data["line_item_type_id"], int)

        if need_cost_code or need_line_item:
            # Make the API call once if we need either value
            cost_code_data = self.cost_codes.find(company_id, project_id, data["cost_code_id"])
            if cost_code_data:
                if need_cost_code:
                    data["cost_code_id"] = int(cost_code_data["id"])
                if need_line_item:
                    line_item_types = cost_code_data.get("line_item_types", [])
                    if not line_item_types:
                        raise ValueError(f"No line item types found for cost code {cost_code_data['id']}")

                    data["line_item_type_id"] = int(line_item_types[0]["id"]) # Take the first one
            else:
                raise ValueError(f"Cost code '{data['cost_code_id']}' not found in project '{project_id}'.")

        # Handle 'date' and 'datetime'
        today = datetime.now()
        if "date" not in data and "datetime" not in data:
            # Both empty, default to today
            data["date"] = today.strftime("%Y-%m-%d")
            data["datetime"] = today.strftime("%Y-%m-%dT12:00:00Z")
        elif "date" not in data:
            # 'date' is empty, use the date from 'datetime'
            dt = datetime.strptime(data["datetime"], "%Y-%m-%dT%H:%M:%SZ")
            data["date"] = dt.strftime("%Y-%m-%d")
        elif "datetime" not in data:
            # 'datetime' is empty, use the 'date' and default time
            dt_date = datetime.strptime(data["date"], "%Y-%m-%d")
            data["datetime"] = dt_date.strftime("%Y-%m-%dT12:00:00Z")

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        # Perform the POST request
        return self.post_request(
            api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timecard_entries",
            additional_headers=headers,
            data={
                "project_id": project_id,
                "timecard_entry": data
            }
        )

    def update(self, company_id, project_id, timecard_id, data):
        """
        Updates the given timecard with the provided data
        https://developers.procore.com/reference/rest/timecard-entries?version=latest#update-timecard-entry-company

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Procore's unique identifier for the project.
        timecard_id : int
            Timecard unique identifier.
        data : dict
            Timecard data to patch.
        """
        headers = {
            "Procore-Company-Id": f"{company_id}",
            "Content-Type": "application/json"
        }

        if "date" not in data.keys():
            raise ValueError("You must provide a 'date' value when updating a timecard entry.")
            
        update_data = {
            "project_id": project_id,
            "timecard_entry": data
        }

        return self.patch_request(
            api_url=f"{self.endpoint}/v1.0/companies/{company_id}/timecard_entries/{timecard_id}",
            data=update_data,
            additional_headers=headers
        )