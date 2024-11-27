import pytest
from unittest.mock import MagicMock
from datetime import datetime
from ProPyCore.access.time.timecards import Timecards  # Adjust the import path as needed


class TestTimecards:
    @pytest.fixture
    def timecards_instance(self, mocker):
        """
        Fixture to create an instance of the Timecards class with mocked dependencies.
        """
        mocker.patch("ProPyCore.access.time.timecards.Base.__init__", return_value=None)  # Mock Base class init
        return Timecards(access_token="mock_access_token", server_url="mock_server_url")

    def test_get_for_day_with_date(self, timecards_instance, mocker):
        """
        Test get_for_day method when entry_date is provided.
        """
        mocker.patch.object(
            timecards_instance,
            "get_request",
            side_effect=[
                [{"id": 1, "hours": 8}, {"id": 2, "hours": 6}],  # First call
                [],  # Second call to break the loop
            ],
        )

        entry_date = datetime(2024, 11, 27)
        timecards = timecards_instance.get_for_day(
            company_id=123,
            project_id=456,
            entry_date=entry_date,
            page=1,
            per_page=10,
        )

        # Validate the total length of returned timecards
        assert len(timecards) == 2

        # Verify the calls made to `get_request`
        expected_calls = [
            mocker.call(
                api_url="/rest/v1.0/projects/456/timecard_entries",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "project_id": 456,
                    "page": 1,
                    "per_page": 10,
                    "log_date": "2024-11-27",
                },
            ),
            mocker.call(
                api_url="/rest/v1.0/projects/456/timecard_entries",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "project_id": 456,
                    "page": 2,
                    "per_page": 10,
                    "log_date": "2024-11-27",
                },
            ),
        ]
        timecards_instance.get_request.assert_has_calls(expected_calls)

    def test_get_for_day_without_date(self, timecards_instance, mocker):
        """
        Test get_for_day method when entry_date is None.
        """
        mocker.patch.object(
            timecards_instance,
            "get_request",
            side_effect=[
                [{"id": 3, "hours": 7}],  # First call
                [],  # Second call to break the loop
            ],
        )

        timecards = timecards_instance.get_for_day(
            company_id=123,
            project_id=456,
            entry_date=None,
            page=1,
            per_page=10,
        )

        # Validate the total length of returned timecards
        assert len(timecards) == 1

        # Verify the calls made to `get_request`
        expected_calls = [
            mocker.call(
                api_url="/rest/v1.0/projects/456/timecard_entries",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "project_id": 456,
                    "page": 1,
                    "per_page": 10,
                },
            ),
            mocker.call(
                api_url="/rest/v1.0/projects/456/timecard_entries",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "project_id": 456,
                    "page": 2,
                    "per_page": 10,
                },
            ),
        ]
        timecards_instance.get_request.assert_has_calls(expected_calls)

    def test_get_for_pay_period(self, timecards_instance, mocker):
        """
        Test get_for_pay_period method.
        """
        mocker.patch.object(
            timecards_instance,
            "get_request",
            side_effect=[
                [{"id": 4, "hours": 5}],  # First call
                [],  # Second call to break the loop
            ],
        )

        timecards = timecards_instance.get_for_pay_period(
            company_id=123,
            page=1,
            per_page=10,
        )

        # Validate the total length of returned timecards
        assert len(timecards) == 1

        # Verify the calls made to `get_request`
        expected_calls = [
            mocker.call(
                api_url="/rest/v1.0/companies/123/timesheets",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "company_id": 123,
                    "page": 1,
                    "per_page": 10,
                },
            ),
            mocker.call(
                api_url="/rest/v1.0/companies/123/timesheets",
                additional_headers={"Procore-Company-Id": "123"},
                params={
                    "company_id": 123,
                    "page": 2,
                    "per_page": 10,
                },
            ),
        ]
        timecards_instance.get_request.assert_has_calls(expected_calls)
