import socket
import struct


class TcpSocket(socket.socket):
    SIZE_HEADER_FORMAT = "00000000|"  # n digits for data size + one delimiter
    size_header_size = len(SIZE_HEADER_FORMAT)
    TCP_DEBUG = False
    LEN_TO_PRINT = 100
    FIELD_DELIMETER = '`' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def recv_by_size(self):
        size_header = b''
        data_len = 0
        while len(size_header) < TcpSocket.size_header_size:
            _s = self.recv(TcpSocket.size_header_size - len(size_header))
            if _s is None:
                size_header = b''
                break
            size_header += _s
        # Now, the size header field has entirely received in size_header (which is binary).
        data = b''
        if size_header != b"":
            data_len = int(size_header[:TcpSocket.size_header_size - 1])
            while len(data) < data_len:
                _d = self.recv(data_len - len(data))
                if _d is None:
                    data = b""
                    break
                data += _d

        if TcpSocket.TCP_DEBUG and size_header is not None:
            print(f"\nRecv({int(size_header[:-1])})>>>{data[:TcpSocket.LEN_TO_PRINT]}")
        if data_len != len(data):
            data = b""  # Partial data is like no data !
        return data


    def send_with_size(self, bdata):
        len_data = len(bdata)
        header_data = str(len(bdata)).zfill(TcpSocket.size_header_size - 1).encode() + b"|"
        if type(bdata) != bytes:
            bdata = bdata.encode()
        bytea = header_data + bdata

        self.send(bytea)
        
        if TcpSocket.TCP_DEBUG and len_data > 0:
            print(f"\nSent({len_data})>>>{bytea[:TcpSocket.LEN_TO_PRINT]}")

        
    def build_request(self, code, *args):
        return code + TcpSocket.FIELD_DELIMETER.join(*args)
    
    def deconstruct_response(self, message):
        code = message[:3]
        fields = message[3:].split(TcpSocket.FIELD_DELIMETER)
        return code, fields
