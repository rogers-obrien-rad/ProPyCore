import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from ProPyCore.procore import Procore
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

    company = connection.companies.find(identifier="Rogers-O`Brien Construction")
    project = connection.projects.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    print(company["id"])
    print(project["id"])

    # Example 1
    # ---------
    print("Example 1")
    dcs = connection.direct_costs.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    print(f"Number of Direct Cost Items: {len(dcs)}")
    print(json.dumps(dcs[0], indent=4))
    
    # Example 2
    # ---------
    print("Example 2")
    direct_cost_id=dcs[0]["id"]
    print(direct_cost_id)
    dc = connection.direct_costs.show(
        company_id=company["id"],
        project_id=project["id"],
        direct_cost_id=direct_cost_id
    )

    print(f"Number of Direct Cost Items: {len(dcs)}")
    print(json.dumps(dc, indent=4))

    # Example 3
    # ---------
    print("Example 3")
    dc_find = connection.direct_costs.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier=direct_cost_id
    )

    print(json.dumps(dc_find, indent=4))

    # Example 3
    # ---------
    print("Example 3")
    try:
        dc_not_found = connection.direct_costs.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier=1
        )

        print(json.dumps(dc_not_found, indent=4))
    except Exception as e:
        print(f"Error: {e}")

    # Example 4
    # ---------
    # Example of creating a Direct Cost item
    direct_cost_data = {
        "description": "Invoice for April",
        "direct_cost_date": "2024-12-14",
        "employee_id": 8780450,
        "invoice_number": "Invoice # abc123",
        "origin_data": "OD-2398273424",
        "origin_id": "px-1990",
        "payment_date": "2025-01-10",
        "received_date": "2025-01-08",
        "status": "approved",
        "terms": "Net 50",
        "vendor_id": 5181441,
        "direct_cost_type": "invoice"
    }

    created_direct_cost = connection.direct_costs.create(
        company_id=company["id"],
        project_id=project["id"],
        direct_cost_data=direct_cost_data,
    )
