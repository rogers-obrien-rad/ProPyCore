from ..base import Base
from ...exceptions import NotFoundItemError

class Punch(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)