from .base import Base
from ..exceptions import NotFoundItemError, NoPrivilegeError, WrongParamsError, ProcoreException

class GenericTool(Base):
    """
    Access and working with generic tool endpoints
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/companies"

    def get(self, company_id, per_page=100):
        """
        Gets all the available generic tools

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        per_page : int, default 100
            number of generic tools to find per page

        Returns
        -------
        tools : dict
            available generic tools
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        # List of generic tools is likely less than 100, but this could lead to errors in the future
        params = {
            "page": 1,
            "per_page": per_page
        }

        tools = self.get_request(
            api_url=f"{self.endpoint}/{company_id}/generic_tools",
            additional_headers=headers,
            params=params
        )

        return tools
    
    def find(self, company_id, identifier):
        """
        Finds a tools based on the identifier: id or title

        Parameters
        ----------
        company_id : int
            company id that the project is under
        identifier : int or str
            project id number or company name
        
        Returns
        -------
        tool : dict
            tool-specific dictionary
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for tool in self.get(company_id=company_id):
            if tool[key] == identifier:
                return tool

        raise NotFoundItemError(f"Could not find tool {identifier}")
    
    def get_items(self, company_id, project_id, tool_id):
        """
        Gets all the available items for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool

        Returns
        -------
        items : dict
            available tool item data
        """
        n_items = 1
        page = 1
        items = []
        while n_items > 0:
            params = {
                "view": "extended",
                "sort": "created_at",
                "page": page,
                "per_page": 10000,
                "filters[recycle_bin]": False
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            item_info = self.get_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items",
                additional_headers=headers,
                params=params
            )

            n_items = len(item_info)
            if n_items > 0:
                items += item_info

            page += 1 

        if len(items) > 0:
            return items
        else:
            raise NotFoundItemError(f"No items are available in Project {project_id} for tool {tool_id}")
    
    def create_item(self, company_id, project_id, tool_id, data):
        """
        Create new item for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool
        data : dict
            request body data for the new item

        Returns
        -------
        item_info : dict
            new item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            item_info = self.post_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items",
                additional_headers=headers,
                data=data
            )
        except ProcoreException as e:
            if "403" in e:
                raise NoPrivilegeError(f"Data connection app or permission template does not allow creation of generic tools")
            else:
                raise WrongParamsError(e)
        
        return item_info
    
    def find_item(self, company_id, project_id, tool_id, identifier):
        """
        Finds a specific generic tool item based on the identifier

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool
        identifier : int or str
            item id number or company name

        Returns
        -------
        tool_item : dict
            response body for the given tool item
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        tool_items = self.get_tool_items(
            company_id=company_id,
            project_id=project_id,
            tool_id=tool_id
        )

        for tool_item in tool_items:
            if tool_item[key] == identifier:
                return tool_item

        raise NotFoundItemError(f"Could not find tool item {identifier}")
    
    def update_item(self, company_id, project_id, tool_id, item_id, data):
        """
        Updates item for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool
        item_id : int
            unique identifier for the item to change
        data : dict
            request body data for the new item

        Returns
        -------
        item_info : dict
            updated response body item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            item_info = self.patch_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items/{item_id}",
                additional_headers=headers,
                data=data
            )
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return item_info
    
    def delete_item(self, company_id, project_id, tool_id, item_id):
        """
        Updates item for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool
        item_id : int
            unique identifier for the item to change

        Returns
        -------
        <status> : str
            status code and text of the delete
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            _ = self.delete_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items/{item_id}",
                additional_headers=headers
            )
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return "200: Success"
    
    def get_statuses(self, company_id, tool_id):
        """
        Gets all the available statuses for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        tool_id : int
            unique identifier for the generic tool

        Returns
        -------
        items : dict
            available tool item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        status_info = self.get_request(
            api_url=f"/rest/v1.0/companies/{company_id}/generic_tools/{tool_id}/available_statuses",
            additional_headers=headers
        )
        
        return status_info
    
    def get_created_statuses(self, company_id, tool_id):
        """
        Gets statuses that were created for a specific tool. Does not include the default statuses that each tool will have.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        tool_id : int
            unique identifier for the generic tool

        Returns
        -------
        items : dict
            available tool item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        status_info = self.get_request(
            api_url=f"/rest/v1.0/companies/{company_id}/generic_tools/{tool_id}/statuses",
            additional_headers=headers
        )
        
        return status_info
    
    def create_status(self, company_id, tool_id, data):
        """
        Create new status for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        tool_id : int
            unique identifier for the generic tool
        data : dict
            request body data for the new item

        Returns
        -------
        status_info : dict
            response from new status creation
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            status_info = self.post_request(
                api_url=f"/rest/v1.0/companies/{company_id}/generic_tools/{tool_id}/statuses",
                additional_headers=headers,
                data=data
            )
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return status_info
    
    def delete_status(self, company_id, tool_id, status_id):
        """
        Delete status for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        tool_id : int
            unique identifier for the generic tool
        status_id : int
            status id for removal

        Returns
        -------
        status_info : dict
            response from new status creation
        """
        
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            _ = self.delete_request(
                api_url=f"/rest/v1.0/companies/{company_id}/generic_tools/{tool_id}/statuses{status_id}",
                additional_headers=headers
            )
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return "200: Success"