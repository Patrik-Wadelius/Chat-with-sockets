import socket
from threading import Thread

class Server:
    # Nya anslutningar läggs till i "Clients"
    Clients = []
    
    #Skapar TCP socket över IPV4
    def __init__(self,HOST,PORT):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((HOST,PORT))
            self.socket.listen()
            print("Inväntar anslutningar...")
        except socket.error as socket_error:
            print(f"Socket error: {socket_error}")
            exit(1) 
    #
    def listen(self):
        while True:
            try:
                client_socket, address = self.socket.accept()
                print("Anslutning: " + str(address))
                
                #första meddelandet kommer vara clientens namn, Sparar sedan clienten med namn och socket i en dict
                client_name = client_socket.recv(1024).decode()
                if not client_name:
                    print(f"Klient skickade inget namn från {address}")
                    client_socket.close()
                    continue
                
                client = {"client_name": client_name, "client_socket": client_socket}
                
                #Meddelar när andra clienter har anslutit och lägger till de i listan "Clients"
                self.broadcast_msg(client_name, client_name + " har anslutit!")
                Server.Clients.append(client)
                
                Thread(target = self.new_client, args = (client,)).start()
            except socket.error as socket_error:
                print(f"Socket error: {socket_error}")
    
    def new_client(self, client):
        client_name = client["client_name"]
        client_socket = client["client_socket"]
        while True:
            #Tar emot meddelanden från client sidan
            client_msg = client_socket.recv(1024).decode()
            #Clienten disconnectar genom klassisk "ggwp"
            if client_msg.strip() == client_name + ": ggwp" or not client_msg.strip():
                self.broadcast_msg(client_name, client_name + " har lämnat!")
                Server.Clients.remove(client)
                break
            else:
                # Skickar meddelande till clienterna
                self.broadcast_msg(client_name, client_msg)
    
    # Loopar igenom clienterna och skickar meddelande till alla clienter,
    # om meddelandet kommer from samma socket skickas detta inte tillbaka
    def broadcast_msg(self, sender_name, message):
        for client in self.Clients:
            client_socket = client["client_socket"]
            client_name = client["client_name"]
            try:
                if client_name != sender_name:
                    client_socket.send(message.encode())
            except socket.error as socket_error:
                print(f"Socket error: {socket_error}")

if __name__ == "__main__":
    server = Server("127.0.0.1", 65535)
    server.listen()