import pytest
import os
from datetime import datetime
from dotenv import load_dotenv
from ProPyCore.procore import Procore

class TestTimecardsIntegration:
    @pytest.fixture(scope="module")
    def procore_connection(self):
        """
        Fixture to establish a Procore connection using sandbox credentials.
        """
        load_dotenv()

        connection = Procore(
            client_id=os.getenv("PROCORE_CLIENT_ID"),
            client_secret=os.getenv("PROCORE_CLIENT_SECRET"),
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",  # default for data connection apps
            oauth_url="https://app.procore.com",  # default for data connection apps
            base_url="https://app.procore.com",  # default for data connection apps
        )

        return connection

    def validate_timecard_structure(self, timecard):
        """
        Validate the structure and required fields of a timecard entry.
        """
        assert isinstance(timecard, dict), "Timecard entry is not a dictionary"
        required_fields = ["id", "created_at", "updated_at"]
        for field in required_fields:
            assert field in timecard, f"Timecard entry missing required field: {field}"
        
    def test_get_for_current_day(self, procore_connection):
        """
        Test fetching timecards for the current day.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        project_id = int(os.getenv("SANDBOX_PROJECT_ID"))

        try:
            timecards = procore_connection.time.timecards.get_for_day(
                company_id=company_id,
                project_id=project_id,
                page=1,
                per_page=10,
            )

            # Validate response
            assert isinstance(timecards, list), "Timecards response is not a list"
            for timecard in timecards:
                self.validate_timecard_structure(timecard)

        except Exception as e:
            pytest.fail(f"Failed to fetch current day timecards: {str(e)}")

    def test_get_for_specified_day(self, procore_connection):
        """
        Test fetching timecards for a specific day.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        project_id = int(os.getenv("SANDBOX_PROJECT_ID"))

        test_date = datetime(2024, 11, 26)
        
        try:
            timecards = procore_connection.time.timecards.get_for_day(
                company_id=company_id,
                project_id=project_id,
                entry_date=test_date,
                page=1,
                per_page=10,
            )

            # Validate response
            assert isinstance(timecards, list), "Timecards response is not a list"
            for timecard in timecards:
                self.validate_timecard_structure(timecard)

        except Exception as e:
            pytest.fail(f"Failed to fetch timecards for {test_date.strftime('%Y-%m-%d')}: {str(e)}")

    def test_get_for_pay_period(self, procore_connection):
        """
        Test fetching timecards for a pay period.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))

        try:
            timecards = procore_connection.time.timesheets.get_for_pay_period(
                company_id=company_id,
                page=1,
                per_page=10,
            )

            # Validate response
            assert isinstance(timecards, list), "Timecards response is not a list"
            for timecard in timecards:
                assert isinstance(timecard, dict), "Timecard entry is not a dictionary"
                assert "timecard_entries" in timecard, "Timecard entry does not contain 'timecard_entries' field"
                if "timecard_entries" in timecard and timecard["timecard_entries"]:
                    for entry in timecard["timecard_entries"]:
                        assert isinstance(entry, dict), "Timecard entry is not a dictionary"
                        assert "hours" in entry, "Timecard entry missing hours field"

        except Exception as e:
            pytest.fail(f"Failed to fetch pay period timecards: {str(e)}")

    def test_get_for_specified_period(self, procore_connection):
        """
        Test fetching timecards for a specific date range.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        
        start_date = datetime(2024, 11, 22)
        end_date = datetime(2024, 11, 28)
        
        try:
            timecards = procore_connection.time.timecards.get_for_specified_period(
                company_id=company_id,
                start_date=start_date,
                end_date=end_date,
                page=1,
                per_page=100,
            )

            # Validate response
            assert isinstance(timecards, list), "Timecards response is not a list"
            for timecard in timecards:
                assert isinstance(timecard, dict), "Timecard entry is not a dictionary"

        except Exception as e:
            pytest.fail(f"Failed to fetch timecards for period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}: {str(e)}")

    def test_invalid_project_id(self, procore_connection):
        """
        Test behavior with an invalid project ID.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        invalid_project_id = 999999999  # Using an invalid project ID

        with pytest.raises(Exception) as exc_info:
            procore_connection.time.timecards.get_for_day(
                company_id=company_id,
                project_id=invalid_project_id,
                page=1,
                per_page=10,
            )
        
        assert exc_info.value is not None, "Expected an error for invalid project ID"