import sys
from controllers import controller

def on_inventory_click():
    controller.navigate("inventory")

def on_sell_click():
    controller.navigate("sell")

def on_receipts_click():
    controller.navigate("receipts")

def on_inventory_transaction_click():
    controller.navigate("inventory_transaction")

def on_exit_click():
    sys.exit()