import socket
import threading 

from dataclasses import dataclass

from protocol.AsyncMessages import AsyncMessages
from protocol.tcp_client import TcpClient
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
        self.socket = TcpClient()
        self.socket.connect(BackendConstants.SERVER_ADDR)
        self.messages = []
        self.errors = []
        self.lock = threading.Lock()

        self.updateThread = threading.Thread(target=self.update, daemon=True)
        self.updateThread.start()

    def login(self, username, password):
        self.socket.send_with_size(self.socket.build_request(ProtocolConstants.CODES["login"], username, password))
        return True

    def register(self, username, email, password, confirmation_password):        
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["register"], username, email, password)
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

    def get_response(self, code):
        code_responses = []
        error_messages = []

        
        for index, message in enumerate(self.messages):
            if message.code == code:
                code_responses.append(message)

                self.messages.pop(index)
                

        for index,error in enumerate(self.errors):
            if error.fields[0].decode() == code:
                error_messages.append(error)

                self.errors.pop(index)


        return code_responses, error_messages

    
    
    

