# **************************************************************** #
#  simple translation of exercise 3 code. use for reference only!  #
# **************************************************************** #

import socket
import struct
import time
import sys

BUFFER_SIZE = 4096


def main():
    # Correct argument input check
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <port> <algorithm>")
        return

    # Transform the information that we get and declaring all the variables and objects
    port = int(sys.argv[1])
    algo = sys.argv[2]

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set congestion control algorithm
    if algo in ["reno", "cubic"]:
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, algo.encode())
    else:
        print("Invalid algorithm")
        return

    # Bind socket to port
    server_socket.bind(('0.0.0.0', port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server is listening on port {port}...")

    # Accept incoming connection
    client_socket, client_addr = server_socket.accept()
    print(f"Client connected from {client_addr[0]}:{client_addr[1]}")

    # Receive file data
    repeat_counter = 0
    name = f"received_file{repeat_counter}.txt"
    file = open(name, "wb")

    # Time measure
    start_time = time.time()

    total_bytes_received = 0

    # Receiving process
    while True:
        bytes_received = client_socket.recv(BUFFER_SIZE)
        if not bytes_received:
            break

        total_bytes_received += len(bytes_received)

        if b"\exit" in bytes_received:
            exit_position = bytes_received.find(b"\exit")
            file.write(bytes_received[:exit_position])
            file.close()

            end_time = time.time()
            total_time = end_time - start_time
            print(f"File received and saved as {name} (Time taken: {total_time:.8f} seconds)")

            average_bandwidth = (total_bytes_received * 8) / (total_time * 1024 * 1024)  # in Mbps
            print(f"Average Bandwidth: {average_bandwidth:.2f} Mbps")

            repeat_counter += 1
            name = f"received_file{repeat_counter}.txt"
            file = open(name, "wb")

            remaining_data = bytes_received[exit_position + len(b"\exit") + 1:]
            file.write(remaining_data)
            start_time = time.time()
            total_bytes_received = len(remaining_data)
            continue
        else:
            file.write(bytes_received)

    # Closing the file
    file.close()

    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()