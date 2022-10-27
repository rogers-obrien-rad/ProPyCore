import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

def find_company(company_list, identifier):
    """
    Finds a company based on the identifier

    Parameters
    ----------
    company_list : list of dict
        companies
    identifier : int or str
        company id number or company name
    
    Returns
    -------
    company : dict
        company-specific dictionary
    """
    # determining which identifier to search for
    if isinstance(identifier, int):
        key = "id"
    else:
        key = "name"

    for company in company_list:
        if company[key] == identifier:
            return company

    return {}

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )
    # get the available companies from the open connection
    companies = connection.__companies__.get()

    # Examples
    # --------
    # find company by name (str)
    company = find_company(companies, identifier="DataPull")
    print(f"{company['id']}: {company['name']}")

    # find company by id (int)
    company = find_company(companies, identifier=3829471)
    print(f"{company['id']}: {company['name']}")

    # non-existent company
    company = find_company(companies, identifier=1)
    print(company)
