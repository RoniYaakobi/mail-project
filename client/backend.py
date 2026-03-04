import socket
import threading 

from dataclasses import dataclass

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

        self.username = None
        self.email = None
        self.password = None
        self.code = None

    def set_password(self, password):
        self.password = password
    
    def reset_password(self):
        self.password = None

    def set_username(self, username):
        self.username = username
    
    def reset_username(self):
        self.username = None

    def get_username(self):
        return self.username

    def set_email(self, email):
        self.email = email
    
    def reset_email(self):
        self.email = None

    def get_email(self):
        return self.email

    def set_code(self, code):
        self.code = code
    
    def reset_code(self):
        self.code = None

    def login(self):
        self.socket.send_with_size(self.socket.build_request(ProtocolConstants.CODES["login"], self.username, self.password))
        return True

    def register(self):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["register"], self.username, self.password , self.email)
        )

        return True
    
    def forgot_password(self):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["forgot"], self.email)
        )

        return True
    
    def reset_password(self):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["reset"], self.email, self.code, self.password)
        )

        return True
    
    def verify_account(self):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["verify"], self.username, self.password, self.code)
        )

        return True
    
    def verify_for_reset(self):
        self.socket.send_with_size(
            self.socket.build_request(ProtocolConstants.CODES["verforgot"], self.email, self.code)
        )

        return True
    
    def reset_code(self, email=False):
        if email:
            self.socket.send_with_size(
                self.socket.build_request(ProtocolConstants.CODES["resendmail"], self.email)
            )
        else:
            self.socket.send_with_size(
                self.socket.build_request(ProtocolConstants.CODES["resend"], self.username)
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
