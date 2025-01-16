from .punch import Punch

class Quality:
    def __init__(self, access_token, server_url):
        self.punch = Punch(access_token, server_url)