from tkinter import messagebox

from client.commands.basic_commands import Command

from protocol.protocol_constants import ProtocolConstants

from client.pages.login import LoginPage


class RegisterCommand(Command):
    def __init__(self, controller, username, email, password, confirm, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.username = username
        self.email = email
        self.password = password
        self.confirm = confirm
        self.username_taken = False
        self.passwords_matching = False
        self.connected = False
        self._initialize = self.initialize
        self._is_finished = self.is_finished
        self._end = self.end

    def initialize(self):
        self.passwords_matching = self.password == self.confirm

        if not self.passwords_matching:
            self.cancel()

        self.connected = self.controller.backend().register(self.username, self.email, self.password, self.confirm)
        if not self.connected:
            self.cancel()

    def is_finished(self):
        messages, errors = self.controller.backend().get_messages_of_type(ProtocolConstants.CODES["register"])
        if len(errors) > 0:
            self.username_taken = True
            self.cancel()
        return len(messages) > 0


    def end(self, interrupted):
        if not interrupted:
            messagebox.showinfo("Register", f"Registered {self.username}")
            self.controller.goto(LoginPage.PAGE_ID)
        elif self.username_taken:
            messagebox.showerror("Register", f"Username {self.username} was taken")
        elif not self.passwords_matching:
            messagebox.showerror("Register", f"Confirmation password was different from password")
        else:
            messagebox.showerror("Register", f"Failed to connect to server!")
