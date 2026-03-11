from tkinter import messagebox

from client.commands.basic_commands import Command

from protocol.protocol_constants import ProtocolConstants

from client.pages.login import LoginPage


class ConnectCommand(Command):
    def __init__(self, controller, cipher_type, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.cipher_type = cipher_type
        self.connected = False
        self._initialize = self.initialize
        self._is_finished = self.is_finished
        self._end = self.end

    def initialize(self):
        self.controller.backend().set_username(self.username)
        self.connected = self.controller.backend().login()

        if not self.connected:
            self.cancel()
            return

    def is_finished(self):
        messages, errors = self.controller.backend().get_messages_of_type(ProtocolConstants.CODES["login"])

        if len(errors) > 0:
            self.has_errors = True
            self.cancel()
            return False

        return len(messages) > 0


    def end(self, interrupted):
        if not interrupted:
            messagebox.showinfo("Login", f"Connected to username: {self.username}")
            
            self.controller.goto(LoginPage.PAGE_ID)
        elif self.has_errors:
            messagebox.showerror("Login", f"Incorrect username or password!")
        else:
            messagebox.showerror("Login", f"Failed to connect to server!")
