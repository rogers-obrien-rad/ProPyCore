from .trades import Trades
from .users import Users
from .vendors import Vendors
from .roles import Roles
from .people import People

class Directory:
    def __init__(self, access_token, server_url):
        self.trades = Trades(access_token, server_url)
        self.users = Users(access_token, server_url)
        self.vendors = Vendors(access_token, server_url)
        self.roles = Roles(access_token, server_url)
        self.people = People(access_token, server_url)