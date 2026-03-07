from database.database import get_all_receipts, get_receipt_by_no
from controllers.receipt_controller import print_pdf, print_usb


class ReceiptsController:
    def __init__(self, page):
        self.page = page
        self.selected_receipt_no = None

    def load_all(self):
        """Return list of (date, time, receipt_no) for the table."""
        return get_all_receipts()

    def select(self, receipt_no):
        self.selected_receipt_no = receipt_no

    def get_selected_cart(self):
        if not self.selected_receipt_no:
            return None, "No receipt selected!"
        cart = get_receipt_by_no(self.selected_receipt_no)
        if not cart:
            return None, "Receipt not found!"
        return cart, None

    def print_selected_pdf(self):
        cart, err = self.get_selected_cart()
        if err:
            return err
        return print_pdf(cart, self.selected_receipt_no)

    def print_selected_usb(self):
        cart, err = self.get_selected_cart()
        if err:
            return err
        return print_usb(cart, self.selected_receipt_no)