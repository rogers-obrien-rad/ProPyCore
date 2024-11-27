import pytest
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from ProPyCore.procore import Procore

# Directories (relative to the script location)
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "samples_responses"
LOG_DIR = BASE_DIR / "logs"

def custom_log(message, level="INFO"):
    """
    Custom logging function to append messages to the log file.

    Parameters
    ----------
    message : str
        The message to log.
    level : str
        The logging level (e.g., INFO, DEBUG, ERROR).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {level} - {message}\n"
    with open(LOG_DIR / "timecard_integration.log", "a") as log_file:
        log_file.write(log_message)

class TestTimecardsIntegration:
    @pytest.fixture(scope="module")
    def procore_connection(self):
        """
        Fixture to establish a Procore connection using sandbox credentials.
        """
        load_dotenv()
        custom_log("Loading environment variables and initializing Procore connection.")

        connection = Procore(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",  # default for data connection apps
            oauth_url="https://app.procore.com",  # default for data connection apps
            base_url="https://app.procore.com",  # default for data connection apps
        )

        return connection

    def save_response(self, filename, data):
        """
        Utility function to save API response data to a JSON file.
        """
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        custom_log(f"Response saved to {filepath}")

    def test_get_for_current_day(self, procore_connection):
        """
        Test fetching timecards for a specific project and save the response.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        project_id = int(os.getenv("SANDBOX_PROJECT_ID"))

        custom_log(f"Fetching timecards for company_id={company_id}, project_id={project_id}.")
        timecards = procore_connection.time.timecards.get_for_day(
            company_id=company_id,
            project_id=project_id,
            page=1,
            per_page=10,
        )
        custom_log(f"Found {len(timecards)} timecards for today.")

        # Save the response to a JSON file
        self.save_response(f"timecards_daily_project.json", timecards)

        # Validate response
        assert isinstance(timecards, list), "Timecards response is not a list."
        if timecards:
            assert isinstance(timecards[0], dict), "Timecard entry is not a dictionary."
            assert "id" in timecards[0], "Timecard entry does not contain 'id'."

    def test_get_for_specified_day(self, procore_connection):
        """
        Test fetching timecards for a specific project and save the response.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))
        project_id = int(os.getenv("SANDBOX_PROJECT_ID"))

        custom_log(f"Fetching timecards for company_id={company_id}, project_id={project_id}.")
        d = datetime(2024,11,26)
        timecards = procore_connection.time.timecards.get_for_day(
            company_id=company_id,
            project_id=project_id,
            entry_date=d,
            page=1,
            per_page=10,
        )
        custom_log(f"Found {len(timecards)} timecards for {datetime.strftime(d, '$Y-$m-$d')}.")

        # Save the response to a JSON file
        self.save_response(f"timecards_daily_project.json", timecards)

        # Validate response
        assert isinstance(timecards, list), "Timecards response is not a list."
        if timecards:
            assert isinstance(timecards[0], dict), "Timecard entry is not a dictionary."
            assert "id" in timecards[0], "Timecard entry does not contain 'id'."

    def test_get_for_pay_period(self, procore_connection):
        """
        Test fetching timecards for a pay period and save the response.
        """
        company_id = int(os.getenv("SANDBOX_COMPANY_ID"))

        custom_log(f"Fetching timecards for company_id={company_id} for a pay period.")
        timecards = procore_connection.time.timecards.get_for_pay_period(
            company_id=company_id,
            page=1,
            per_page=10,
        )
        custom_log(f"Found {len(timecards)} timecards for the current pay period.")

        # Save the response to a JSON file
        self.save_response(f"timecards_pay_period.json", timecards)

        # Validate response
        assert isinstance(timecards, list), "Timecards response is not a list."
        if timecards:
            assert isinstance(timecards[0], dict), "Timecard entry is not a dictionary."
            assert "timecard_entries" in timecards[0], "Timecard entry does not contain 'timecard_entries' field."