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

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # Example 1: Search for file with multiple perfect matches
    # ---------
    print("Example 1")
    doc1 = connection.__files__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="test"
    )
    print(f"{doc1['id']}: {doc1['name']}")
    # warn("Multiple 100% matches - try refining your search critera for better results")
    # 607851830: test_pdf.pdf
    
    # Example 1: Search for private file
    # ---------
    print("\nExample 2")
    doc2 = connection.__files__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="another"
    )
    print(f"{doc2['id']}: {doc2['name']}")
    # 607851830: another_test_pdf.pdf
    
    # Example 3: Find folder 
    # ---------
    print("\nExample 3")
    doc3 = connection.__folders__.search(
        company_id=company["id"],
        project_id=project["id"],
        value="training"
    )
    print(f"{doc3['id']}: {doc3['name']}")
    # 607846718: 3-Orientations and Training

    # Example 4: Find file in subfolder 
    # ---------
    print("\nExample 4")
    folder = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="I-Safety and Environmental"
    )
    doc4 = connection.__files__.search(
        company_id=company["id"],
        project_id=project["id"],
        folder_id=folder["id"],
        value="test"
    )
    print(f"{doc4['id']}: {doc4['name']}")
    # 607851830: another_test_pdf.pdf
    
    # Example 5: Find subfolder in specified folder 
    # ---------
    print("\nExample 5")
    folder = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="I-Safety and Environmental"
    )
    doc5 = connection.__folders__.search(
        company_id=company["id"],
        project_id=project["id"],
        folder_id=folder["id"],
        value="subcontractor"
    )
    print(f"{doc5['id']}: {doc5['name']}")
    # 607846791: Subcontractors Orientation