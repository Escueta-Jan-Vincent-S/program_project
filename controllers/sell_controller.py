from database.database import get_item_by_barcode, update_item, save_receipt
import controllers.controller as c


class SellController:
    def __init__(self, page):
        self.page = page
        self.cart = []
        self.cash_input = ""
        self.mode = "manual"  # "manual" or "scan"

    # ── Cart Management ───────────────────────────────────────
    def add_by_barcode(self, barcode):
        barcode = barcode.strip()
        if not barcode:
            return "Please enter a barcode!"

        item = get_item_by_barcode(barcode)
        if not item:
            return f"Item not found: {barcode}"

        item_name     = item[2]
        selling_price = float(item[5])
        current_stock = int(item[6])

        if current_stock <= 0:
            return f"'{item_name}' is out of stock!"

        for cart_item in self.cart:
            if cart_item["barcode"] == barcode:
                if cart_item["quantity"] >= current_stock:
                    return "Not enough stock!"
                cart_item["quantity"] += 1
                return None  # success

        self.cart.append({
            "barcode": barcode,
            "item_name": item_name,
            "selling_price": selling_price,
            "quantity": 1
        })
        return None  # success

    def increment(self, barcode):
        for item in self.cart:
            if item["barcode"] == barcode:
                db_item = get_item_by_barcode(barcode)
                max_stock = int(db_item[6]) if db_item else 999
                if item["quantity"] < max_stock:
                    item["quantity"] += 1
                return

    def decrement(self, barcode):
        for item in self.cart:
            if item["barcode"] == barcode:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    self.cart.remove(item)
                return

    def remove_item(self, barcode):
        self.cart = [i for i in self.cart if i["barcode"] != barcode]

    def clear_cart(self):
        self.cart = []
        self.cash_input = ""

    def get_total(self):
        return sum(i["selling_price"] * i["quantity"] for i in self.cart)

    # ── Numpad ────────────────────────────────────────────────
    def numpad_press(self, digit):
        if len(self.cash_input) < 10:
            self.cash_input += digit

    def numpad_backspace(self):
        self.cash_input = self.cash_input[:-1]

    def numpad_clear(self):
        self.cash_input = ""

    def get_cash(self):
        return float(self.cash_input) if self.cash_input else 0.0

    def get_change(self):
        return max(0.0, self.get_cash() - self.get_total())

    # ── Payment ───────────────────────────────────────────────
    def process_payment(self):
        if not self.cart:
            return None, "Cart is empty!"

        if not self.cash_input:
            return None, "Please enter cash amount!"

        cash  = self.get_cash()
        total = self.get_total()

        if cash < total:
            return None, f"Insufficient cash!\nTotal: ₱{total:.2f}\nCash: ₱{cash:.2f}"

        # Deduct stock
        for item in self.cart:
            db_item = get_item_by_barcode(item["barcode"])
            if db_item:
                new_stock = max(0, int(db_item[6]) - item["quantity"])
                update_item(item["barcode"], db_item[2], db_item[3],
                            float(db_item[4]), float(db_item[5]), new_stock)

        # Save to receipts table
        receipt_no = save_receipt(self.cart, total, cash, self.get_change())

        return receipt_no, None  # success