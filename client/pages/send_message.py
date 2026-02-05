from client.pages.page import Page, PageType
from tkinter import messagebox


class MessengerPage(Page):
    PAGE_ID = PageType.assign_id("messenger")
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.set_title("Welcome to Messenger")

        self.recipent = self.create_field("Recipent:")
        self.recipent.pack()

        self.message = self.create_field("Message:")
        self.message.pack()
        

        self.create_action_button("Send", self.send_action, pack_pady=5)
        
        self.add_link(page_type=PageType.identify("login"), text="Back to Login")

    def send_action(self):
        recipent = self.recipent.get()
        message = self.message.get()
        messagebox.showinfo("Sent Message", f"Password reset link sent to {recipent}!")

