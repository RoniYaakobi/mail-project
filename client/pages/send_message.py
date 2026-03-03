from tkinter import messagebox

from protocol.protocol_constants import ProtocolConstants
from client.pages.page import Page, PageType
from client.commands.send_message_command import SendMessageCommand



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
        recipents = self.recipent.get().split(",")
        message = self.message.get()

        self.messages.append(f"You: {message}")

        self.scheduler().schedule(SendMessageCommand(self, message, recipents))
        
        

    def update_errors(self):
        new_errors, _ = self.backend().get_messages_of_type(ProtocolConstants.CODES["error"])
        
        new_errors = [f"{new_error.code}: {",".join(new_error.fields)}" for new_error in new_errors]
        self.errors += new_errors

    def get_errors(self):
        return "\n".join(self.errors)
    
    def update_messages(self):
        new_messages, _ = self.backend().get_messages_of_type(ProtocolConstants.CODES["recieve"])
        
        new_messages = [f"{message.fields[0]}: {message.fields[1]}" for message in new_messages]
        self.messages += new_messages

    def get_messages(self):
        return "\n".join(self.messages)
