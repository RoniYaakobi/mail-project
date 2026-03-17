__author__ = "RONI YAAKOBI"
from tkinter import messagebox

from client.commands.basic_commands import Command

from protocol.protocol_constants import ProtocolConstants

class SendMessageCommand(Command):
    def __init__(self, controller, message, recipents, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.message = message
        self.recipents = recipents
        self.connected = False
        self._initialize = self.initialize
        self._end = self.end

    def initialize(self):
        self.connected = self.controller.backend().send_message(self.message, self.recipents)
        if not self.connected:
            self.cancel()
            return

    def end(self, interrupted):
        if interrupted:
            messagebox.showerror("Messenger", f"Failed to connect to server!")
