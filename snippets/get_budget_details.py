import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv
import json

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    budget_view = connection.__budgets__.find_view(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Detailed Budget View"
    )

    # Example 1: List all columns
    # ---------
    print("Example 1")
    budget_columns = connection.__budgets__.get_budget_columns(
        company_id=company["id"],
        project_id=project["id"],
        budget_view_id=budget_view["id"]
    )

    print(f"Number of Budget Columns: {len(budget_columns)}")

    # Example 2: Find column by name
    # ---------
    print("Example 2")
    column_by_name = connection.__budgets__.find_budget_column(
        company_id=company["id"],
        project_id=project["id"],
        budget_view_id=budget_view["id"],
        identifier="Cost to Date"
    )

    print(json.dumps(column_by_name, indent=4))

    # Example 3: List all rows
    # ---------
    print("Example 3")
    budget_rows = connection.__budgets__.get_budget_rows(
        company_id=company["id"],
        project_id=project["id"],
        budget_view_id=budget_view["id"]
    )

    print(f"Number of Budget Rows: {len(budget_rows)}")
    # Uncomment to save budget rows
    #with open("rows.json", "w") as f:
    #    json.dump(budget_rows, f, indent=4)

    # Example 4: Find row by name
    # ---------
    print("Example 4")
    row_by_name = connection.__budgets__.find_budget_row(
        company_id=company["id"],
        project_id=project["id"],
        budget_view_id=budget_view["id"],
        identifier="None"
    )

    print(json.dumps(row_by_name, indent=4))

    # Example 5: Get budget details
    # ---------
    # TODO: Getting ClientNotFoundError
    '''
    print("Example 5")
    details = connection.__budgets__.get_budget_details(
        company_id=company["id"],
        project_id=project["id"],
        budget_view_id=budget_view["id"]
    )

    print(f"Number of budget line items: {len(details)}")
    '''