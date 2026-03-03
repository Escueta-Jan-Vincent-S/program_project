import customtkinter as ctk
from settings import APP_NAME, WINDOW_SIZE

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.attributes("-fullscreen", True)

def open_window():
    app = Dashboard()
    app.mainloop()