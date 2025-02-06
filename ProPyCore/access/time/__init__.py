from .timecards import Timecards
from .timesheets import Timesheets

class Time:
    
    def __init__(self, access_token, server_url):
        self.timecards = Timecards(access_token, server_url)
        self.timesheets = Timesheets(access_token, server_url)