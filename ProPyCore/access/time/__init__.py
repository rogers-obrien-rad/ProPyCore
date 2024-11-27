from .timecards import Timecards

class Time:
    def __init__(self, access_token, server_url):
        self.timecards = Timecards(access_token, server_url)