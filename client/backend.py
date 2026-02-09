import socket

from protocol.AsyncMessages import AsyncMessages
from protocol.tcp_socket import TcpSocket
from protocol.protocol_constants import ProtocolConstants


class AppBackend:
    def __init__(self):
        super().__init__()
        self.socket = TcpSocket()
        self.socket.connect()

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

    def recv_message(self):
        message = self.socket.recv_by_size()
        code, fields = self.socket.deconstruct_response(message)
            
        return code == ProtocolConstants.CODES["error"], fields
    
    
    

