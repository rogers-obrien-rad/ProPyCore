from ..base import Base
from ...exceptions import NotFoundItemError

class Trades(Base):
    """Access vendor information on a Company and Project Level"""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/companies"

    def get(self, company_id, per_page=1000):
        """
        Gets a list of all the trades the company level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        per_page : int, default 1000
            number of companies to include

        Returns
        -------
        users : list of dict
            list where each value is a dict with a user's information
        """
        trades = []
        n_trades = 1
        page = 1
        while n_trades > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "company_id": company_id
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            trades_per_page = self.get_request(
                api_url=f"{self.endpoint}/{company_id}/trades",
                additional_headers=headers,
                params=params
            )
            n_trades = len(trades_per_page)

            trades += trades_per_page
            page += 1

        return trades

    def find(self, company_id, user_id):
        """
        Finds a trade based on the identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        user_id : int or str
            project id number or company name
        
        Returns
        -------
        trade : dict
            trade-specific dictionary
        """
        if isinstance(user_id, int):
            key = "id"
        else:
            key = "name"

        for trade in self.get(company_id=company_id):
            if trade[key] == user_id:
                return trade

        raise NotFoundItemError(f"Could not find {user_id}")
