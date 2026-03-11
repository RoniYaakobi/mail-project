import struct, os
from protocol.protocol_constants import ProtocolConstants
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from protocol.tcp_socket import TcpSocket
from client.backend_constants import BackendConstants


class TcpClient(TcpSocket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aes_key = TcpClient.generate_aes_key()

    def set_addr(self, addr):
        self.addr = addr
        
    def build_request(self, code, *args):
        print(args)
        return code + TcpClient.FIELD_DELIMETER.join(args)
    

    def deconstruct_response(self, message):
        code = message[:3].decode()
        fields = message[3:].decode().split(TcpClient.FIELD_DELIMETER)
        return code, fields
    
    def validate_server_support(self, encryption_type):
        self.send(struct.pack("!B", encryption_type.value))
        return struct.unpack("!B", self.recv(1))[0] == 1
    
    def connect_rsa(self):
        self.connect(self.addr)
        server_supports_method = self.validate_server_support(ProtocolConstants.EncryptionType.RSA)
        if not server_supports_method:
            self.connected = False
            return False
        
        self.raw_send_with_size(ProtocolConstants.ACK)
        public_key_bytes = self.raw_recv_by_size()
        self.server_public_key = serialization.load_pem_public_key(public_key_bytes)

        self.send_aes_with_rsa()
        self.response = self.recv_by_size()

        if self.response.decode() == ProtocolConstants.ACK:
            self.connected = True
            return True
        else:
            print("Error: Server failed to respond with AES ack")
            self.connected = False
            return False

    def send_aes_with_rsa(self):
        aes_key = self.server_public_key.encrypt(
            self.aes_key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),  
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        self.raw_send_with_size(aes_key)

    def connect_dh(self):
        pass

    @staticmethod
    def generate_aes_key():
        return os.urandom(32)
    
if __name__ == "__main__":
    client = TcpClient()
    client.set_addr(BackendConstants.SERVER_ADDR)
    print(client.connect_rsa())
    client.send_with_size("YAY")
