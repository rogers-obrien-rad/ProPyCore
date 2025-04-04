from .base import Base
from ..exceptions import WrongParamsError, ProcoreException

class Permissions(Base):
    """
    Access and working with permissions endpoints
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0"
        
    def get(self, company_id, project_id=None) -> dict:
        """
        Gets all the available permissions

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            Include for project-level permissions

        Returns
        -------
        permissions : dict
            available permissions
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        params = {}
        if project_id is not None:
            params["project_id"] = project_id
        else:
            params["company_id"] = company_id

        try:
            response = self.get_request(self.endpoint + "/settings/permissions", additional_headers=headers, params=params)
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return response

    def get_company_templates(self, company_id) -> dict:
        """
        Gets all the available company templates

        Parameters
        ----------
        company_id : int
            unique identifier for the company

        Returns
        -------
        company_templates : dict
            available company templates
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            response = self.get_request(self.endpoint + f"/companies/{company_id}/permission_templates", additional_headers=headers)
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return response

    def get_company_template(self, company_id, template_id) -> dict:
        """
        Gets a specific company template

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        template_id : int
            unique identifier for the template

        Returns
        -------
        company_template : dict
            available company template
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            response = self.get_request(self.endpoint + f"/companies/{company_id}/permission_templates/{template_id}", additional_headers=headers)
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return response

    def get_project_templates(self, company_id, project_id) -> dict:
        """
        Gets all the available project templates

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        project_templates : dict
            available project templates
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            response = self.get_request(self.endpoint + f"/projects/{project_id}/permission_templates", additional_headers=headers)
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return response