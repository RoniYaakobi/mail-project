import tkinter as tk
from tkinter import messagebox
from client.pages.forgot_password import ForgotPage
from client.pages.login import LoginPage
from client.pages.signup import SignUpPage
from client.pages.send_message import MessengerPage
from client.commands.basic_commands import CommandScheduler


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_page = None

        self.title("My App")
        self.geometry("400x300")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.scheduler = CommandScheduler(self,10)

        self.pages = {}

        for PageClass in (LoginPage, SignUpPage, ForgotPage, MessengerPage):
            page = PageClass(container, self)
            self.pages[PageClass.PAGE_ID] = page

            page.grid(row=0, column=0, sticky="nsew")

        for page in self.pages.values():
            for page_id in page.get_links().keys():

                page.set_link(page_id, self.pages.get(page_id,page))


        self.show_page(LoginPage.PAGE_ID)

        self.scheduler.periodic()

    def show_page(self, page_class):
        self.pages[page_class].show()
        self.current_page = page_class

if __name__ == "__main__":
    app = App()
    app.mainloop()

