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

        self.errors = []
        self.create_text_box("Errors", self.update_errors, self.get_errors, pack_padx=5, pack_pady=5)
        
        self.messages = []
        self.create_text_box("Messages", self.update_messages, self.get_messages, pack_padx=5, pack_pady=5)

        self.create_action_button("Send", self.send_action, pack_pady=5)
        
        self.add_link(page_type=PageType.identify("login"), text="Back to Login")

    def send_action(self):
        recipent = self.recipent.get()
        message = self.message.get()
        self.messages.append(message)
        messagebox.showinfo("Sent Message", f"Sent message to {recipent}!")

    def update_errors(self):
        self.errors = ["bruh"]

    def get_errors(self):
        return "\n".join(self.errors)
    
    def update_messages(self):
        pass

    def get_messages(self):
        return "\n".join(self.messages)
