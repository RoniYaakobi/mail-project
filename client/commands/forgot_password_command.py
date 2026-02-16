from tkinter import messagebox

from client.commands.basic_commands import Command

from protocol.protocol_constants import ProtocolConstants


class ForgotPasswordCommand(Command):
    def __init__(self, controller, email, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.email = email
        self.connected = False
        self.has_errors = False
        self._initialize = self.initialize
        self._is_finished = self.is_finished
        self._end = self.end

    def initialize(self):
        self.connected = self.controller.backend().forgot_password(self.email)
        if not self.connected:
            self.cancel()

    def is_finished(self):
        messages, errors = self.controller.backend().get_response(ProtocolConstants.CODES["forgot"])

        if len(errors) > 0:
            self.has_errors = True
            self.cancel()

        return len(messages) > 0


    def end(self, interrupted):
        if not interrupted:
            messagebox.showinfo("Forgot Password", f"Sent reset email to {self.email}")
        elif self.has_errors:
            messagebox.showerror("Forgot Password", f"Failed to send reset email.")
        else:
            messagebox.showerror("Forgot Password", f"Failed to connect to server!")
