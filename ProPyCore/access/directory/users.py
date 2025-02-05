from ..base import Base
from ...exceptions import NotFoundItemError

class Users(Base):
    """Access user information on a Company and Project Level"""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def get_url(self, company_id, project_id=None):
        """
        Returns the url specific to Users at company or project level

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
            url for Users request
        """
        if project_id is None:
            return f"/rest/v1.1/companies/{company_id}/users"
        else:
            return f"/rest/v1.0/projects/{project_id}/users"

    def get(self, company_id, project_id=None, per_page=1000):
        """
        Gets a list of all the users from the company or project level

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
        users : list of dict
            list where each value is a dict with a user's information
        """
        users = []
        n_users = 1
        page = 1
        while n_users > 0:
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

            users_per_page = self.get_request(
                api_url=url,
                additional_headers=headers,
                params=params
            )
            n_users = len(users_per_page)

            users += users_per_page
            page += 1

        return users

    def show(self, company_id, project_id, user_id):
        """
        Shows a user's details

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        user_id : int
            unique identifier for the user

        Returns
        -------
        user : dict
            user-specific dictionary
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        if project_id is None:
            url = f"/rest/v1.3/companies/{company_id}/users/{user_id}"
        else:
            url = f"/rest/v1.0/projects/{project_id}/users/{user_id}"
    
        return self.get_request(
            api_url=url,
            additional_headers=headers,
        )
    
    def find(self, company_id, user_id, project_id=None,):
        """
        Finds a user based on their Procore identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        user_id : int or str
            if int, search by user id
            if str with @, search by user email
            else, search by user name
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        
        Returns
        -------
        user : dict
            user-specific dictionary
        """
        if isinstance(user_id, int):
            key = "id"
        elif "@" in user_id:
            key = "email_address"
        else:
            key = "name"

        for user in self.get(company_id=company_id, project_id=project_id):
            if user[key] == user_id:
                return user

        raise NotFoundItemError(f"Could not find User {user_id}")

    def add(self, company_id, project_id, user_id, permission_template_id=None):
        """
        Adds a company user to a given project

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project to add the user to
        user_id : int
            unique identifier of the user to add
        permission_template_id : int, default None
            level of permissions to give the added user
        """
        data = {
            "user":{
                "permission_template_id": permission_template_id,
            }
        }

        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        self.post_request(
            api_url=f"/rest/v1.0/projects/{project_id}/users/{user_id}/actions/add",
            additional_headers=headers,
            params=params,
            data=data
        )