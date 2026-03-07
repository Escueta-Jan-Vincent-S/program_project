import customtkinter as ctk
from controllers import controller
from controllers.receipt_controller import print_pdf, print_usb
from datetime import datetime
import random

class ReceiptPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#90EE90", corner_radius=0)
        self.cart = []
        self.receipt_no = ""

        # ── Header ──────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#90EE90", height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkButton(
            header, text="<", fg_color="transparent",
            text_color="#000000", hover_color="#7dd67d",
            font=ctk.CTkFont(size=40, weight="bold"),
            corner_radius=0, width=60, height=60,
            command=lambda: controller.navigate("inventory")
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            header, text="OFFICIAL RECEIPT",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#000000"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkFrame(self, fg_color="#000000", height=2, corner_radius=0).pack(fill="x")

        # ── Body ─────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="#90EE90", corner_radius=0)
        body.pack(fill="both", expand=True)

        # ── Receipt Card ─────────────────────────────────────
        self.card = ctk.CTkFrame(body, fg_color="#ffffff", corner_radius=0,
                                  border_color="#000000", border_width=2,
                                  width=500)
        self.card.place(relx=0.4, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # ── Right side buttons ────────────────────────────────
        right = ctk.CTkFrame(body, fg_color="#90EE90", corner_radius=0)
        right.place(relx=0.82, rely=0.5, anchor="center")

        ctk.CTkButton(
            right, text="🖨️  USB Thermal",
            fg_color="#d3d3d3", text_color="#000000",
            hover_color="#c0c0c0", border_color="#000000", border_width=2,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=0, width=200, height=50,
            command=self.do_usb_print
        ).pack(pady=5)

        ctk.CTkButton(
            right, text="📄  Save as PDF",
            fg_color="#90EE90", text_color="#000000",
            hover_color="#7dd67d", border_color="#000000", border_width=2,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=0, width=200, height=50,
            command=self.do_pdf_print
        ).pack(pady=5)

    def load_receipt(self, cart):
        self.cart = cart
        self.receipt_no = f"REC-{random.randint(10000, 99999)}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Clear card
        for widget in self.card.winfo_children():
            widget.destroy()

        # Store info
        ctk.CTkLabel(self.card, text="LANZ & LINDLY MINIMART",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000").pack(pady=(15, 0))
        ctk.CTkLabel(self.card, text="****ADDRESS****",
            font=ctk.CTkFont(size=12), text_color="#000000").pack()
        ctk.CTkLabel(self.card, text="TEL. NO.",
            font=ctk.CTkFont(size=12), text_color="#000000").pack()
        ctk.CTkLabel(self.card, text=f"RECEIPT NO. {self.receipt_no}",
            font=ctk.CTkFont(size=12), text_color="#000000").pack()
        ctk.CTkLabel(self.card, text=now,
            font=ctk.CTkFont(size=11), text_color="#000000").pack(pady=(0, 5))

        ctk.CTkFrame(self.card, fg_color="#000000", height=1, corner_radius=0).pack(fill="x", padx=10)
        ctk.CTkLabel(self.card, text="RECEIPT",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000").pack(pady=5)
        ctk.CTkFrame(self.card, fg_color="#000000", height=1, corner_radius=0).pack(fill="x", padx=10)

        # Column headers
        col_frame = ctk.CTkFrame(self.card, fg_color="#ffffff", corner_radius=0)
        col_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(col_frame, text="DESCRIPTION",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#000000").pack(side="left")
        ctk.CTkLabel(col_frame, text="PRICE",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#000000").pack(side="right")

        # Items
        total = 0
        for item in cart:
            amount = item["selling_price"] * item["quantity"]
            total += amount

            row = ctk.CTkFrame(self.card, fg_color="#ffffff", corner_radius=0)
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row,
                text=f"{item['item_name']} x{item['quantity']}",
                font=ctk.CTkFont(size=12), text_color="#000000").pack(side="left")
            ctk.CTkLabel(row,
                text=f"₱{amount:.2f}",
                font=ctk.CTkFont(size=12), text_color="#000000").pack(side="right")

        ctk.CTkFrame(self.card, fg_color="#000000", height=1, corner_radius=0).pack(fill="x", padx=10, pady=5)

        # Total / Cash / Change
        for label, value in [
            ("TOTAL",  f"₱{total:.2f}"),
            ("CASH",   "₱0.00"),
            ("CHANGE", "₱0.00")
        ]:
            row = ctk.CTkFrame(self.card, fg_color="#ffffff", corner_radius=0)
            row.pack(fill="x", padx=10)
            ctk.CTkLabel(row, text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#000000").pack(side="left")
            ctk.CTkLabel(row, text=value,
                font=ctk.CTkFont(size=13), text_color="#000000").pack(side="right")

        ctk.CTkFrame(self.card, fg_color="#000000", height=1, corner_radius=0).pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.card, text="THANK YOU",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000").pack(pady=(0, 15))

    def do_usb_print(self):
        result = print_usb(self.cart, self.receipt_no)
        self._show_result(result)

    def do_pdf_print(self):
        result = print_pdf(self.cart, self.receipt_no)
        self._show_result(result)

    def _show_result(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Print")
        popup.geometry("350x150")
        popup.resizable(False, False)
        popup.grab_set()
        ctk.CTkLabel(popup, text=message,
            font=ctk.CTkFont(size=14), justify="center").pack(expand=True)
        ctk.CTkButton(popup, text="OK", command=popup.destroy,
            fg_color="#d3d3d3", text_color="#000000",
            corner_radius=0, width=100).pack(pady=10)