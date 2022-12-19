import os
import sys
import pathlib
PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent.parent}"
sys.path.insert(0, PATH_TO_TOP)
from dotenv import load_dotenv

from propycore import procore

from snippets import auth

class TestAuth:

    def test_get_auth_code(self):
        auth_code = auth.get_auth_code()
        assert auth_code is not None

    def test_get_token(self):
        auth_code = auth.get_auth_code()
        access_token, _ = auth.get_token(auth_code)
        assert access_token is not None

class TestFind:

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

    def test_companies(self):
        company_info = self.connection.__companies__.find(
            identifier="DataPull"
        )
        assert company_info is dict

    def test_projects(self):
        company = self.connection.__companies__.find(
            identifier="DataPull"
        )
        project_info = self.connection.__projects__.find(
            company_id=company["id"],
            identifier="R&D Test Project"
        )
        assert project_info is dict

    def test_folders(self):
        company = self.connection.__companies__.find(
            identifier="DataPull"
        )
        project = self.connection.__projects__.find(
            company_id=company["id"],
            identifier="R&D Test Project"
        )
        folder = self.connection.__folders__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="Subcontractors Orientation"
        )
        assert folder is dict

    def test_files(self):
        company = self.connection.__companies__.find(
            identifier="DataPull"
        )
        project = self.connection.__projects__.find(
            company_id=company["id"],
            identifier="R&D Test Project"
        )
        file = self.connection.__files__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="Masonry Checklist.txt"
        )
        assert file is dict

    def test_rfis(self):
        company = self.connection.__companies__.find(
            identifier="DataPull"
        )
        project = self.connection.__projects__.find(
            company_id=company["id"],
            identifier="Sandbox Test Project"
        )
        rfi = self.connection.__rfis__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="1",
        )
        assert rfi is dict