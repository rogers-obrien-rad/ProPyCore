import os
import sys
import pathlib
PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent.parent}"
sys.path.insert(0, PATH_TO_TOP)

from dotenv import load_dotenv

from propycore import procore

class TestFunctionality:

    def __init__(self) -> None:

        if os.getenv("CLIENT_ID") is None:
            load_dotenv()

        self.connection = procore.Procore(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URI"),
            oauth_url=os.getenv("OAUTH_URL"),
            base_url=os.getenv("BASE_URL")
        )

    def test_connection(self):
        assert self.connection is not None

    def test_company_listing(self):
        temp_company_list = self.connection.__companies__.get()
        assert temp_company_list is list

    def test_project_listing(self):
        company_list = self.connection.__companies__.get()
        temp_company = company_list[0]
        temp_projects = self.connection.__projects__.get(company_id=temp_company)
        assert temp_projects is list

    def test_find_company(self):
        company = self.connection.find_company(identifier="DataPull")
        assert company is dict

    def test_find_project(self):
        company = self.connection.find_company(identifier="DataPull")
        project = self.connection.find_project(
            company_id=company["id"],
            identifier="R&D test Project"
        )
        assert project is dict

    def test_find_dir(self):
        dir_ids = self.connection.find_dir(
            company="DataPull",
            project="R&D Test Project",
            folderpath="/I-Safety and Environmental/3-Orientations and Training/Subcontractors Orientation"
        )
        assert dir_ids is list

if __name__ == "__main__":
    test_connection = TestFunctionality()