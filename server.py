import socket
import pickle
from threading import Thread

from chat import Chat
from constants import SERVER_ADDR


def threaded_client(client_socket: socket.socket, chat: Chat):
    while True:
        try:
            message = pickle.loads(client_socket.recv(4096))
            chat.add_message(**message)
        except ConnectionResetError:
            chat.remove_socket(client_socket)
            print("[LOST] connection to one client lost")
            return


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen()

    connections = -1
    chats = []

    print("[READY] ready to accept connections ...")

    while True:
        client_socket, addr = server_socket.accept()
        connections += 1

        print(f"[NEW] new connection, total: {str(connections+1)}")

        if connections//2 >= len(chats):
            chats.append(Chat(len(chats), {client_socket}))
            print(f"[CREATED] new Chat created, total: {str(len(chats))}")
        else:
            chats[-1].add_socket(client_socket)
        
        client_thread = Thread(target=threaded_client, args=(client_socket, chats[-1]))
        client_thread.start()
