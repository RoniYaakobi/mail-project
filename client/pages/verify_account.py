from client.pages.page import Page, PageType
from tkinter import messagebox

from client.commands.verify_command import VerifyCommand
from client.commands.resend_command import ResendCommand


class VerifyPage(Page):
    PAGE_ID = PageType.assign_id("verify")
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.set_title(text="verify")

        self.verification_code = self.create_field(text="Code")
        self.verification_code.pack()


        self.create_action_button("verify", self.verification_action, pack_pady=5)
        self.create_action_button("resend", self.resend_code_action, pack_pady=5)
        self.add_link(page_type=PageType.identify("signup"), text="Back To Register")

    def verification_action(self):
        username = self.global_state().get("username")
        password = self.global_state().get("password")

        code = self.verification_code.get()

        self.scheduler().schedule(VerifyCommand(self, username, password, code))

    def resend_code_action(self):
        username = self.global_state().get("username")
        password = self.global_state().get("password")

        self.scheduler().schedule(ResendCommand(self, username, password,))
