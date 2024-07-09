from .base import Base
from ..exceptions import *

class Task(Base):
    """
    Access and working with submittals in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/tasks"

    def get(self, company_id, project_id):
        """
        Gets all the available tasks

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        tasks : dict
            available submittal data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        n_tasks = 1
        page = 1
        tasks = []
        while n_tasks > 0:

            params = {
                "project_id": project_id,
                "page": page,
                "per_page": 100
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            task_selection = self.get_request(
                api_url=f"{self.endpoint}",
                additional_headers=headers,
                params=params
            )

            n_tasks = len(task_selection)
            tasks += task_selection
            page += 1 

        return tasks
    
    def show(self, company_id, project_id, task_id):
        """
        Shows the task info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        task_id : int
            unique identifier for the task

        Returns
        -------
        task_info : dict
            specific task information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        params = {
            "project_id": project_id,
        }

        task_info = self.get_request(
            api_url=f"{self.endpoint}/{task_id}",
            additional_headers=headers,
            params=params
        )

        return task_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified tasks and returns data

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for task which can be id (int) or name (str)

        Returns
        -------
        task_info : dict
            task data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for task in self.get(company_id=company_id, project_id=project_id):
            if task[key] == identifier:
                task_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    task_id=task["id"]
                )
                return task_info

        raise NotFoundItemError(f"Could not find task {identifier}")