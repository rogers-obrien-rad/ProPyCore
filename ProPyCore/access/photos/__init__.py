from .categories import Categories
from .images import Images

class Photos:
    def __init__(self, access_token, server_url):
        self.categories = Categories(access_token, server_url)
        self.images = Images(access_token, server_url)