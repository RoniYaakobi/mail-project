import socket
import struct
import types


class ClientSocketWrapper:
    def __init__(self, sock):
        self.sock = sock
        self.username = ""

    def recv_by_size(self, *args, **kwargs):
        return TcpServer.recv_by_size(self.sock, *args, **kwargs)

    def send_with_size(self, *args, **kwargs):
        return TcpServer.send_with_size(self.sock, *args, **kwargs)

    def build_response(self, *args, **kwargs):
        
        return TcpServer.build_response(self.sock, *args, **kwargs)

    def deconstruct_request(self, *args, **kwargs):
        return TcpServer.deconstruct_request(self.sock, *args, **kwargs)



class TcpServer(socket.socket):
    SIZE_HEADER_FORMAT = "00000000|"  # n digits for data size + one delimiter
    size_header_size = len(SIZE_HEADER_FORMAT)
    TCP_DEBUG = True
    LEN_TO_PRINT = 100
    FIELD_DELIMETER = '`' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def recv_by_size(self):
        size_header = b''
        data_len = 0
        while len(size_header) < TcpServer.size_header_size:
            _s = self.recv(TcpServer.size_header_size - len(size_header))
            if _s is None:
                size_header = b''
                break
            size_header += _s
        # Now, the size header field has entirely received in size_header (which is binary).
        data = b''
        if size_header != b"":
            data_len = int(size_header[:TcpServer.size_header_size - 1])
            while len(data) < data_len:
                _d = self.recv(data_len - len(data))
                if _d is None:
                    data = b""
                    break
                data += _d

        if TcpServer.TCP_DEBUG and size_header is not None:
            print(f"\nRecv({int(size_header[:-1])})>>>{data[:TcpServer.LEN_TO_PRINT]}")
        if data_len != len(data):
            data = b""  # Partial data is like no data !
        return data


    def send_with_size(self, bdata):
        len_data = len(bdata)
        header_data = str(len(bdata)).zfill(TcpServer.size_header_size - 1).encode() + b"|"
        if type(bdata) != bytes:
            bdata = bdata.encode()
        bytea = header_data + bdata

        self.send(bytea)
        
        if TcpServer.TCP_DEBUG and len_data > 0:
            print(f"\nSent({len_data})>>>{bytea[:TcpServer.LEN_TO_PRINT]}")

        
    def build_response(self, code, *args):
        return code + TcpServer.FIELD_DELIMETER.join(args)
    
    def deconstruct_request(self, message):
        code = message[:3].decode()
        fields = message[3:].decode().split(TcpServer.FIELD_DELIMETER)
        return code, fields
