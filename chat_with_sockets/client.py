import socket
from threading import Thread
import os

class Client:
    # Ansluter till servern, ber "clienten" att ange ett namn
    def __init__(self, HOST, PORT):
        try:
            self.socket = socket.socket()
            self.socket.connect((HOST, PORT))
            print("Ansluten till servern")
            self.name = input("Ange användarnamn: ")
            print(("\033[31;40m Ange 'ggwp' för att lämna!\033[0m"))
            self.handle_server()
        except socket.error as socket_error:
            print(f"Socket error: {socket_error}")
        
    # Skickar användarnamn, startar sedan en ny "tråd" för att ta,
    # emot meddelanden. Kallar på send_msg för att skicka meddelanden
    def handle_server(self):
        self.socket.send(self.name.encode())
        Thread(target = self.recv_msg).start()
        self.send_msg()
        
    # Hanterar clientens input som skickas ut på servern (Namn: INPUT)
    def send_msg(self):
        while True:
            client_input = input("")
            client_msg = self.name + ": " + client_input
            self.socket.send(client_msg.encode())
            
    # Lyssnar efter nya meddelanden på server, stänger ned om ingen respons från,
    # servern finns
    def recv_msg(self):
        while True:
            try:
                server_msg = self.socket.recv(1024).decode()
                if not server_msg.strip(): 
                    print("Ingen respons från server")
                    os._exit(0)
                print(server_msg)
            except socket.error as socket_error:
                print(f"socket error: {socket_error}")

if __name__ == "__main__":
    Client("127.0.0.1", 65535)