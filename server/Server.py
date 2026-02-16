import threading
import time

from protocol.tcp_server import TcpServer, ClientSocketWrapper
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
            client = ClientSocketWrapper(client)
            thread = threading.Thread(target=self.deal_with_async_client, args=(client,))
            self.async_messages.add_new_socket(client)
            self.clients_to_threads[client] = [False, thread]
            thread.start()
            

    def deal_with_async_client(self, client):
        listen_thread = threading.Thread(target=self.listen_to_client, args=(client,))
        update_thread = threading.Thread(target=self.update_client_messages, args=(client,))
        business_logic= threading.Thread(target=self.business_logic, args=(client,))
        self.clients_to_threads[client] += [listen_thread, update_thread, business_logic]
        listen_thread.start()
        update_thread.start()
        business_logic.start()
        
        
        listen_thread.join()
        update_thread.join()
        business_logic.join()

        del self.clients_to_threads[client]

        self.async_messages.delete_socket(client)

    def update_client_messages(self, client):
        while True:
            with self.thread_dict_lock:
                terminate = self.clients_to_threads[client][0]
                if terminate:
                    break
            
            curr_async_messages = self.async_messages.get_async_messages_to_send(client)
            for msg in curr_async_messages:
                client.send_with_size(
                    client.build_response(ProtocolConstants.CODES["recieve"], *msg)
                )
            time.sleep(0.1)


    def listen_to_client(self, client):
        while True:
            
            with self.thread_dict_lock:
                terminate = self.clients_to_threads[client][0]
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

    def business_logic(self, client: TcpServer):
        while True:
            with self.thread_dict_lock:
                terminate = self.clients_to_threads[client][0]
                if terminate:
                    break
            
            with self.lock:
                try:
                    requests = self.sock_to_requests[client]
                    self.sock_to_requests[client] = []
                except KeyError:
                    requests = []
                    self.sock_to_requests[client] = []

            for request in requests:
                code, fields = self.server.deconstruct_request(request)
                if code == ProtocolConstants.CODES["login"]:
                    is_valid = self.login(fields, client)
                    if is_valid:
                        client.send_with_size(
                            client.build_response(code)
                        )
                    else:
                        client.send_with_size(
                            client.build_response(ProtocolConstants.CODES["error"], code)
                        )


                elif code == ProtocolConstants.CODES["register"]:
                    is_valid = self.register(fields)
                    if is_valid:
                        client.send_with_size(
                            client.build_response(code)
                        )
                    else:
                        client.send_with_size(
                            client.build_response(ProtocolConstants.CODES["error"], code, "USERNAME TAKEN")
                        )

                elif code == ProtocolConstants.CODES["send"]:
                    is_valid = self.send_message(fields, client)

            


    def login(self, fields, client):
        username = fields[0]
        password = fields[1]

        if not (DataBase.IsUserExist(username) and DataBase.IsPasswordOK(username, password)):
            return False 
        
        self.async_messages.connect_user(client, username)
        client.username = username
        return True
    

    def register(self, fields):
        username = fields[0]
        password = fields[1]
        email = fields[2]


        if DataBase.IsUserExist(username):
            return False
        
        DataBase.SaveUser(username, password, email)
        return True


    def send_message(self, fields, client):
        message = fields[0]
        
        for user in fields[1:]:
            if not DataBase.IsUserExist(user):
                return False
            
        for user in fields[1:]:
            self.async_messages.put_msg_by_user((client.username, message), user)
        
        return True

if __name__ == "__main__":
    Server()
