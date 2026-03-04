from controllers import controller
from database.database import get_all_accounts, switch_account

def on_back_click():
    controller.navigate("dashboard")

def get_accounts():
    return get_all_accounts()

def on_switch_account(account_id, refresh_callback):
    switch_account(account_id)
    refresh_callback()