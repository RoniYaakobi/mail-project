import struct

from protocol.tcp_socket import TcpSocket
from protocol.protocol_constants import ProtocolConstants
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class ClientSocketWrapper:
    def __init__(self, sock):
        self.sock = sock
        self.aes_key = None

    def connect_secure(self,**ciphers):
        choice = self.recv(1)
        self.encryption_type = ProtocolConstants.EncryptionType(struct.unpack("!B", choice)[0])

        match(self.encryption_type):
            case ProtocolConstants.EncryptionType.RSA:
                self.send(struct.pack("!B",True))
                return self.connect_secure_rsa(ciphers.get("rsa_private_key"), ciphers.get("rsa_public_key"))
            case ProtocolConstants.EncryptionType.DH:
                self.send(struct.pack("!B",True))
                return self.connect_secure_dh(ciphers.get("dh_parameters"))
            case _:
                self.send(struct.pack("!B",False))
                self.connected = False

    def connect_secure_rsa(self, rsa_private_key, rsa_public_key):
        client_message = self.raw_recv_by_size()
        if client_message.decode() != ProtocolConstants.ACK:
            self.connected = False
            return False
        
        public_key_bytes = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.raw_send_with_size(public_key_bytes)

        aes_key_encrypted = self.raw_recv_by_size()

        self.aes_key = rsa_private_key.decrypt(
            aes_key_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        self.send_with_size(ProtocolConstants.ACK)
        self.connected = True
        return True
    
    def connect_secure_dh(self, dh_parameters):
        client_message = self.raw_recv_by_size()
        if client_message.decode() != ProtocolConstants.ACK:
            self.connected = False
            return False
        
        params_bytes = dh_parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.ParameterFormat.PKCS3)

        self.send_with_size(ProtocolConstants.ACK)
        self.connected = True
        return True
        
        

    def recv(self, num_bytes):
        return self.sock.recv(num_bytes)
    
    def send(self, buffer):
        return self.sock.send(buffer)

    def recv_by_size(self, *args, **kwargs):
        return TcpConnection.recv_by_size(self, *args, **kwargs)

    def send_with_size(self, *args, **kwargs):
        return TcpConnection.send_with_size(self, *args, **kwargs)
    
    def raw_recv_by_size(self, *args, **kwargs):
        return TcpConnection.raw_recv_by_size(self, *args, **kwargs)

    def raw_send_with_size(self, *args, **kwargs):
        return TcpConnection.raw_send_with_size(self, *args, **kwargs)

    def build_response(self, *args, **kwargs):
        return TcpConnection.build_response(self, *args, **kwargs)

    def deconstruct_request(self, *args, **kwargs):
        return TcpConnection.deconstruct_request(self, *args, **kwargs)



class TcpConnection(TcpSocket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_response(self, code, *args):
        return code + TcpSocket.FIELD_DELIMETER.join(args)
    
    def deconstruct_request(self, message):
        code = message[:3].decode()
        fields = message[3:].decode().split(TcpSocket.FIELD_DELIMETER)
        return code, fields


if __name__ == "__main__":
    from cryptography.hazmat.primitives.asymmetric import dh
    from cryptography.hazmat.primitives import serialization
    import os,socket

    RSA_PATH = r"C:\Users\roniy\software_engeeniering\11th\finalProject\server"
    PRIVATE_PATH = os.path.join(RSA_PATH, "RSA_private.pem")
    PUBLIC_PATH = os.path.join(RSA_PATH, "RSA_public.pem")

    def generate_keys():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Save private key (PKCS8 + PEM)
        with open(PRIVATE_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Save public key (SPKI + PEM)
        with open(PUBLIC_PATH, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        print(f"RSA keys generated!")


    def load_private_key():
        with open(PRIVATE_PATH, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def load_public_key():
        with open(PUBLIC_PATH, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    
    if not os.path.exists(PRIVATE_PATH) or not os.path.exists(PUBLIC_PATH):
        generate_keys()

    private_key = load_private_key()
    public_key = load_public_key()

    server_sock = socket.socket()

    import server.server_constants
    server_sock.bind(server.server_constants.ServerConstants.ADDR)
    server_sock.listen(5)
    client_socket,_ = server_sock.accept()
    client = ClientSocketWrapper(client_socket)
    print(client.connect_secure(rsa_private_key=private_key, rsa_public_key=public_key))
    print(client.recv_by_size())


