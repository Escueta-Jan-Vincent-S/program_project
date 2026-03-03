import customtkinter as ctk

class TestWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Test Window")
        self.geometry("1280x720")
        self.resizable(False, False)

def open_window():
    app = TestWindow()
    app.mainloop()