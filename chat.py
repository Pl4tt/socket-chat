import pickle
import socket
import time


class Chat:
    def __init__(self, chat_id: int, member_sockets: set[socket.socket]):
        self.id = chat_id
        self.member_sockets = member_sockets
        self.messages = []
        self.time_created = time.time()

    def add_message(self, author: str, message: str):        
        msg_dict = {
            "author": author,
            "message": message,
        }
        self.messages.append(msg_dict)
        
        for socket in self.member_sockets:
            socket.send(pickle.dumps(msg_dict))
    
    def add_socket(self, socket: socket.socket):
        self.member_sockets.add(socket)
    
    def remove_socket(self, socket: socket.socket):
        self.member_sockets.discard(socket)

