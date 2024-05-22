import socket
import string
import random
import QUIC_Packet


def send_message(server_ip, server_port, message):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cid_length = 16
    cid_characters = string.ascii_letters + string.digits

    try:
        connection_id = ''.join(random.choice(cid_characters) for _ in range(cid_length))
        ivan = QUIC_Packet.Packet(1,"anitaaaaa")

        # Send the message to the server
        client_socket.sendto(ivan.quicEncode(), (server_ip, server_port))
        print(f"Message sent to {server_ip}:{server_port}")

        # Receive the response from the server
        response, server_address = client_socket.recvfrom(1024)
        print(f"Received response from server: {response.decode()}")

    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    send_message("127.0.0.1", 12345, "Hello, UDP Server!")
