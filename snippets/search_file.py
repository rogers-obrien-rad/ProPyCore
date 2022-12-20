import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError

from dotenv import load_dotenv

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

    company = connection.__companies__.find(identifier="DataPull")
    project = connection.__projects__.find(company_id=company["id"], identifier="R&D Test Project")

    # Example 1: Search for public file
    # ---------
    doc1 = connection.__files__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="hagen"
    )
    print(doc1)
    # {'id': 10893611, 'created_at': '2022-11-11T18:36:13Z', 'created_by': {'id': 94241, 'company_name': '', 'locale': None, 'login': 'ro-data-connection-7e2e9a8e@procore.com', 'name': ' ro-data-connection-7e2e9a8e'}, 'custom_fields': {}, 'document_type': 'file', 'is_deleted': False, 'is_recycle_bin': False, 'name': 'rogers-obrien-rd_engineer-fritz-hagen-2022-11-11.pdf', 'name_with_path': 'R&D Test Project/I-Safety and Environmental/3-Orientations and Training/Subcontractors Orientation/rogers-obrien-rd_engineer-fritz-hagen-2022-11-11.pdf', 'parent_id': 10857736, 'private': False, 'read_only': False, 'updated_at': '2022-11-11T18:36:13Z', 'search_critera': {'value': 'hagen', 'match': 100}}

    # Example 1: Search for private file
    # ---------
    doc2 = connection.__files__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="another"
    )
    print(doc2)
    # {'id': 10874954, 'created_at': '2022-11-02T19:01:20Z', 'created_by': {'id': 93809, 'company_name': '', 'locale': None, 'login': 'datapull-8c71be1b@procore.com', 'name': ' datapull-8c71be1b'}, 'custom_fields': {}, 'document_type': 'file', 'is_deleted': False, 'is_recycle_bin': False, 'name': 'another_test_pdf.pdf', 'name_with_path': 'R&D Test Project/I-Safety and Environmental/another_test_pdf.pdf', 'parent_id': 10857734, 'private': True, 'read_only': False, 'updated_at': '2022-11-02T19:01:25Z', 'search_critera': {'value': 'another', 'match': 100}}

    # Example 3: Find folder 
    # ---------
    print("\nExample 3")
    doc3 = connection.__folders__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="safety"
    )
    print(doc3)
    # {'id': 10857734, 'created_at': '2022-10-25T13:47:34Z', 'created_by': {'id': 93688, 'company_name': "Rogers O'Brien Construction", 'locale': None, 'login': 'hfritz@r-o.com', 'name': 'Hagen Fritz'}, 'custom_fields': {}, 'document_type': 'folder', 'is_deleted': False, 'is_recycle_bin': False, 'name': 'I-Safety and Environmental', 'name_with_path': 'R&D Test Project/I-Safety and Environmental', 'parent_id': 10857730, 'private': False, 'read_only': False, 'updated_at': '2022-10-25T13:47:34Z', 'search_critera': {'value': 'safety', 'match': 83}} 
    
    # Example 4: Find subfolders in specified folder 
    # ---------
    print("\nExample 4")
    folder = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="I-Safety and Environmental"
    )
    doc4 = connection.__folders__.search(
        company_id=company["id"],
        project_id=project["id"],
        folder_id=folder["id"],
        value="subcontractor"
    )
    print(doc4)