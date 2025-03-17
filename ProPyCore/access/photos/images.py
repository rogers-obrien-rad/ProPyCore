from ..base import Base
from ...exceptions import NotFoundItemError, ProcoreException

class Images(Base):
    """
    Access and working with Images with App access
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0"