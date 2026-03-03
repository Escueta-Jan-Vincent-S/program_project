# ============================================================
# DASHBOARD WINDOW
# ============================================================

import customtkinter as ctk
from settings import APP_NAME

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.attributes("-fullscreen", True)

        ctk.set_appearance_mode("light")

        # ── Header ──────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#000000", height=150, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="INVENTORY MANAGEMENT SYSTEM",
            font=ctk.CTkFont(size=50, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=10)

        # ── Body ─────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        body.pack(fill="both", expand=True)

def open_window():
    app = Dashboard()
    app.mainloop()

def open_window():
    app = Dashboard()
    app.mainloop()