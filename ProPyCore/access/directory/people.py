from ..base import Base
from ...exceptions import NotFoundItemError

class People(Base):
    """Access user information on a Company and Project Level"""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def get_url(self, company_id, project_id=None):
        """
        Returns the url specific to People at company or project level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level

        Returns
        -------
        <get_url> : str
            url for People request
        """
        if project_id is None:
            return f"/rest/v1.0/companies/{company_id}/people"
        else:
            return f"/rest/v1.0/projects/{project_id}/people"

    def get(self, company_id, project_id=None, per_page=1000):
        """
        Gets a list of all people from the company or project level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        people : list of dict
            list where each value is a dict with a person's information
        """
        people = []
        n_people = 1
        page = 1
        while n_people > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "company_id": company_id # this parameter is only used in Company Vendors, but including it for other requests does not seem to create any issues
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            url = self.get_url(
                company_id=company_id,
                project_id=project_id
            )

            people_per_page = self.get_request(
                api_url=url,
                additional_headers=headers,
                params=params
            )
            n_people = len(people_per_page)

            people += people_per_page
            page += 1

        return people
    
    def find(self, company_id, person_id, project_id=None,):
        """
        Finds a person based on their Procore identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        person_id : int or str
            if int, search by person id
            if str with @, search by person email
            else, search by person name
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        
        Returns
        -------
        person : dict
            person-specific dictionary
        """
        if isinstance(person_id, int):
            key = "id"
        elif isinstance(person_id, str) and "@" in person_id:
            key = "contact"
            subkey = "email"
        else:
            raise TypeError(f"Invalid person_id type or format: {person_id}. Must be an integer ID or email string.")

        for person in self.get(company_id=company_id, project_id=project_id):
            if key == "contact":
                if person.get(key, {}).get(subkey) == person_id:
                    return person
            elif person[key] == person_id:
                return person

        raise NotFoundItemError(f"Could not find Person {person_id}")
