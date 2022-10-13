import os
import sys
import pathlib
PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent.parent}"
sys.path.insert(0, PATH_TO_TOP)

from propycore import procore

class TestFunctionality:

    def __init__(self) -> None:

        self.connection = procore.Procore(
            client_id=os.getenv("TEST_CLIENT_ID"),
            client_secret=os.getenv("TEST_CLIENT_SECRET"),
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            oauth_url="https://sandbox.procore.com",
            base_url="https://sandbox.procore.com"
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

if __name__ == "__main__":
    test_connection = TestFunctionality()