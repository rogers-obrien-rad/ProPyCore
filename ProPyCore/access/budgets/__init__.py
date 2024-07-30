from .views import BudgetViews
from .columns import BudgetColumns
from .rows import BudgetRows

class Budgets:
    def __init__(self, access_token, server_url):
        self.views = BudgetViews(access_token, server_url)
        self.columns = BudgetColumns(access_token, server_url)
        self.rows = BudgetRows(access_token, server_url)