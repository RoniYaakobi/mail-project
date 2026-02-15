import socket
import threading 

from dataclasses import dataclass

from protocol.AsyncMessages import AsyncMessages
from protocol.tcp_socket import TcpSocket
from protocol.protocol_constants import ProtocolConstants
from client.backend_constants import BackendConstants

@dataclass 
class Message:
    code: str
    fields: list

@dataclass
class ErrorMessage(Message):
    pass

class AppBackend:
    def __init__(self):
        super().__init__()
        self.socket = TcpSocket()
        self.socket.connect(BackendConstants.SERVER_ADDR)
        self.messages = []
        self.errors = []
        self.lock = threading.lock()

        self.updateThread = threading.Thread(target=self.update, daemon=True)
        self.updateThread.start()

    def login(self, username, password):
        self.socket.send_with_size(self.socket.build_request(ProtocolConstants.CODES["login"], username, password))

    def regsiter(self, email, username, password, confirmation_password):
        if password != confirmation_password:
            return False
        
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["register"], email, username, password)
        )

        return True
    
    def forgot_password(self, email):
        return False

    def send_message(self, username, message):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["send"], username, message)
        )

    def update(self):
        while True:
            message = self.socket.recv_by_size()
            code, fields = self.socket.deconstruct_response(message)
                
            with self.lock:
                if code != ProtocolConstants.CODES["error"]:
                    self.messages.append(Message(code,fields))
                else:
                    self.errors.append(ErrorMessage(fields[0],fields[1:]))
    
    
    

