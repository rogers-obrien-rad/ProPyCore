import os

from propycore import procore

class TestFunctionality:

    def __init__(self) -> None:

        self.connection = procore.Procore(
            client_id=os.getenv("TEST_CLIENT_ID"),
            client_secret=os.getenv("TEST_CLIENT_SECRET"),
            redirect_uri=os.getenv("TEST_REDIRECT_URI"),
            oauth_url=os.getenv("TEST_OAUTH_URL"),
            base_url=os.getenv("TEST_BASE_URL")
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
    print("yay!")