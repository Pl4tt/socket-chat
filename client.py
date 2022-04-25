import socket
import pickle
from threading import Thread

from constants import SERVER_ADDR


class Client:
    def __init__(self, name: str, server_addr: tuple[str, int]):
        self.name = name
        self.server_addr = server_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()

    def connect(self):
        self.socket.connect(self.server_addr)

    def disconnect(self):
        self.socket.close()

    def send_msg(self, msg: str):
        msg_dict = {
            "author": self.name,
            "message": msg,
        }
        self.socket.send(pickle.dumps(msg_dict))
    
    def receive_msg_task(self, bufsize: int):
        while True:
            msg = pickle.loads(self.socket.recv(bufsize))

            if msg.get("author") != self.name:
                print(f"\r{msg.get('author')}: {msg.get('message')}")


if __name__ == "__main__":
    name = input("Enter your name: ")
    client = Client(name, SERVER_ADDR)

    message_receiver = Thread(target=client.receive_msg_task, args=(4096,))
    message_receiver.start()

    while True:
        msg = input("")
        client.send_msg(msg)
            
        
        
