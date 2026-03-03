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
    handled: bool = False

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

    def register(self, username, email, password):        
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["register"], username, password , email)
        )

        return True
    
    def forgot_password(self, email):
        return False
    
    def verify_account(self, username, password, code):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["verify"], username, password, code)
        )

        return True
    
    def reset_code(self, username, password):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["resend"], username, password)
        )

        return True

    def send_message(self, message, recipents):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["send"], message, *recipents)
        )
        return True

    def update(self):
        while True:
            message = self.socket.recv_by_size()
            code, fields = self.socket.deconstruct_response(message)
                
            with self.lock:
                self.messages.append(Message(code,fields))
                if code == ProtocolConstants.CODES["error"]:
                    self.errors.append(ErrorMessage(fields[0],fields[1:]))
                print(self.messages)
                   

    def get_messages_of_type(self, code):
        code_responses = []
        error_messages = []

        with self.lock:
            for index, message in enumerate(self.messages):
                if message.code == code:
                    code_responses.append(message)

                    self.messages.pop(index)
                    


            remove_indices = []
            for index,error in enumerate(self.errors):
                if error.code == code:
                    error_messages.append(error)

                    remove_indices.append(index)

            for i in remove_indices[::-1]:
                self.errors.pop(i)


        return code_responses, error_messages
