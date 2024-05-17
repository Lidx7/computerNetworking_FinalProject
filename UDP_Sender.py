import socket
import struct
import random
import string
import os

RENO = "reno"
CUBIC = "cubic"
MIN_SIZE = 2097152


# Helper function to generate random data
def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()


# Helper function to send data to the receiver
def send_data(sock, data):
    sentd = sock.send(data)
    if sentd == -1:
        print("Error: send")
        exit(1)
    elif sentd == 0:
        print("Receiver doesn't accept requests.")
    elif sentd < len(data):
        print(f"Data was only partly sent ({sentd}/{len(data)} bytes).")
    else:
        print(f"Total bytes sent is {sentd}.")
    return sentd


def main():
    # Correct argument input check
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <IP> <port> <algorithm>")
        return

    ip = sys.argv[1]
    port = int(sys.argv[2])
    algo = sys.argv[3]

    # Enter desired size of the random file
    file_size = 0
    while file_size < MIN_SIZE:
        file_size = int(input("Enter the size of the file to be sent (minimum size is 2MB): "))

    rand_file = generate_random_data(file_size)

    # Creating socket
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if network_socket < 0:
        print("Error in creating socket")
        return

    # Setting the congestion control algorithm
    if algo in [RENO, CUBIC]:
        network_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, algo.encode())
    else:
        print("Invalid algorithm")
        return

    # Binding the socket to the port and IP
    server_address = (ip, port)

    # Connecting
    try:
        network_socket.connect(server_address)
    except socket.error as e:
        print(f"Error in connecting to server: {e}")
        return

    # Sending the file and repeating as long as the user wants
    while True:
        send_data(network_socket, rand_file)
        send_data(network_socket, b"\exit")

        again = input("Do you want to send the file again? type y for yes, any other character for no: ")
        if again.lower() != 'y':
            break

    # Closing the socket
    network_socket.close()


if __name__ == "__main__":
    import sys

    main()
