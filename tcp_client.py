# Assignment: TCP Simple Chat Room - TCP Client Code Implementation

# **Libraries and Imports**:
import sys
import socket
import argparse
import threading
import select

# **Function Definitions**:

def send_msg(clientSocket):
    """Send messages from this client to the server."""
    while True:
        # Wait for user input
        msg = input()
        clientSocket.sendall(msg.encode('utf-8'))
        if msg.lower() in ['!disconnect', '!exit']:
            clientSocket.sendall(msg.encode("utf-8"))
            break

def receive_msg(clientSocket):
    """Receive and print messages from the server."""
    while True:
        try:
            # Continuously receive data from the server
            data = clientSocket.recv(1024)
            if data:
                # Print the received message
                print(data.decode('utf-8'))
            else:
                # If data is not received, it probably means the server has disconnected
                print("Disconnected from the server.")
                clientSocket.close()
                sys.exit(0)
        except (KeyboardInterrupt):
            print("disconnected")
            break

def run(clientSocket, clientname):
    """Main client function."""
    # Start threads to handle sending and receiving messages
    threading.Thread(target=send_msg, args=(clientSocket,)).start()
    print(f"\n{clientname}'s chat section\n")
    threading.Thread(target=receive_msg, args=(clientSocket,)).start()

# **Main Code**:  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python tcp_client.py username
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    client_socket.connect((server_addr, server_port))

    # Send client name to the server
    client_socket.sendall(client_name.encode('utf-8'))

    run(client_socket, client_name)
