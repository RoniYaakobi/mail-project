import threading

from protocol.tcp_server import TcpServer
from protocol.AsyncMessages import AsyncMessages
from protocol.protocol_constants import ProtocolConstants
from server.server_constants import ServerConstants
from server.database import DataBase

class Server:
    def __init__(self):
        self.server = TcpServer()
        self.server.bind(ServerConstants.ADDR)
        self.server.listen(5)
        self.async_messages = AsyncMessages()
        self.lock = threading.Lock()
        self.thread_dict_lock = threading.Lock()
        self.sock_to_requests = {}

        self.clients_to_threads = {}

        DataBase.load()

        while True:
            client,_ = self.server.accept()
            thread = threading.Thread(target=self.deal_with_async_client, args=(client,))
            self.async_messages.add_new_socket(client)
            thread.start()
            self.clients_to_threads[client] = [False, thread]
            

    def deal_with_async_client(self, client):
        listen_thread = threading.Thread(target=self.listen_to_client, args=(client,))
        business_logic= threading.Thread(target=self.business_logic, args=(client,))
        listen_thread.start()
        business_logic.start()
        self.clients_to_threads[client] += [listen_thread, business_logic]
        
        listen_thread.join()
        business_logic.join()

        del self.clients_to_threads[client]

        self.async_messages.delete_socket(client)


    def listen_to_client(self, client: TcpServer):
        while True:
            with self.thread_dict_lock:
                terminate = self.clients_to_threads[0]
                if terminate:
                    break

            try:
                msg = client.recv_by_size()
                if not msg:
                    break
            except:
                self.clients_to_threads[0] = True # terimination
                break

            with self.lock:
                if self.sock_to_requests.get(client):
                    self.sock_to_requests[client].append(msg)
                else:
                    self.sock_to_requests[client] = [msg]

            client.send_with_size(ProtocolConstants.CODES["receive"], self.async_messages.get_async_messages_to_send(client))

    def business_logic(self, client: TcpServer):
        while True:
            with self.thread_dict_lock:
                terminate = self.clients_to_threads[0]
                if terminate:
                    break
            
            with self.lock:
                requests = self.sock_to_requests[client]
                self.sock_to_requests[client] = []

            for request in requests:
                code, fields = self.server.deconstruct_request(request)
                if code == ProtocolConstants.CODES["login"]:
                    is_valid = self.login(fields, client)
                    if is_valid:
                        client.send_with_size(code)
                    else:
                        client.send_with_size(ProtocolConstants.CODES["error"], code)


                elif code == ProtocolConstants.CODES["register"]:
                    is_valid = self.register(fields)
                    if is_valid:
                        client.send_with_size(code)
                    else:
                        client.send_with_size(ProtocolConstants.CODES["error"], code, "USERNAME TAKEN")


                elif code == ProtocolConstants.CODES["send"]:
                    is_valid = self.send_message(fields)
                    if is_valid:
                        client.send_with_size(code)
                    else:
                        client.send_with_size(ProtocolConstants.CODES["error"], code, "WHO?")

            


    def login(self, fields, client):
        username = fields[0].decode()
        password = fields[1].decode()

        if not (DataBase.IsUserExist(username) and DataBase.IsPasswordOK(username, password)):
            return False 
        
        self.async_messages.connect_user(client, fields[0].decode())
        return True
    

    def register(self, fields):
        username = fields[0].decode()
        password = fields[1].decode()
        email = fields[2].decode()


        if DataBase.IsUserExist(username):
            return False
        
        DataBase.SaveUser(username, password, email)
        return True


    def send_message(self, fields):
        message = fields[0].decode()
        
        for user in fields[1:]:
            if not DataBase.IsUserExist(user):
                return False
            
        for user in fields[1:]:
            self.async_messages.put_msg_by_user(message, user)
        
        return True

if __name__ == "__main__":
    Server()
