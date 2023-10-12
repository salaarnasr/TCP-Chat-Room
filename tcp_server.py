# Assignment: TCP Simple Chat Room - TCP Server Code Implementation


# **Libraries and Imports**:
import socket
import threading
import sys

BUFFER_SIZE = 2048
# **Global Variables**:
clients = []  # List to store connected client sockets

# **Function Definitions**:

def broadcast(message, sender_socket=None):
    """
    Send a broadcast message to all clients.
    """
    for client in clients:
        if client != sender_socket:  # Don't send the message back to the sender
            try:
                client.send(message.encode("utf-8"))
            except:
                client.close()
                if client in clients:
                    clients.remove(client)


def handle_client(client_socket, client_address):
    global clients

    client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")  # First message is always the client's name
    print(f"{client_name} has joined the chatroom.")
    broadcast(f"{client_name} has joined the chatroom.", client_socket)

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if not message:
                break
            # Check for disconnect command
            if message.lower() in ['!disconnect', '!exit']:
                broadcast(f"{client_name} has left the chatroom.", client_socket)
                break

            # If not a disconnect command, broadcast the received message
            broadcast(f"{client_name}: {message}", client_socket)

        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError, KeyboardInterrupt):
            # When client abruptly disconnects
            broadcast(f"{client_name} has left the chatroom.", client_socket)
            break

    # Close the client's socket and remove it from the list after they've disconnected
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)
    print(f"{client_name} disconnected.")



    # Remove the client from our list of clients
    
    client_socket.close()

def run(serverSocket, serverPort):
    """Main server function"""
    global clients

    print("[*] Server started and listening on port:", serverPort)

    try:
        while True:
            client_sock, client_addr = serverSocket.accept()
            print(f"New connection from {client_addr}")
            clients.append(client_sock)
            
            # Start a new thread to handle this specific client
            threading.Thread(target=handle_client, args=(client_sock, client_addr)).start()

    except KeyboardInterrupt:
        print("\n[*] Server shut down.")
        serverSocket.close()


# **Main Code**:
if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3)  # size of the waiting queue

    # Notes about the listen() method...
    # ... [explanation here as provided in your template]

    run(server_socket, server_port)  # Calling the function to start the server
