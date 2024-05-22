import socket
import random
import string
import QUIC_Packet


def start_server(ip, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the provided IP and port
    server_socket.bind((ip, port))
    print(f"UDP server listening on {ip}:{port}")
    response, server_address = server_socket.recvfrom(1024)
    substring  = QUIC_Packet.turn_backString(response.decode())
    packet =QUIC_Packet.LargePacket(substring[0], substring[1])
    if substring[1]=="sinq":
        server_socket.sendto(QUIC_Packet.turn_toString(packet).encode(),server_address)
    # cid_length = 16
    # cid_characters = string.ascii_letters + string.digits
    #
    # while True:
    #     connection_id = ''.join(random.choice(cid_characters) for _ in range(cid_length))
    #
    #     # Receive message from client
    #     message, client_address = server_socket.recvfrom(1024)
    #     print(f"Received message from {client_address}: {message.decode()}")
    #
    #     # Send a response back to the client
    #     response = f"Received your message: {message.decode()}"
    #
    #     ivan = QUIC_Packet.Packet(2, response)
    #     server_socket.sendto(QUIC_Packet.quicDecode(ivan), client_address)
    server_socket.close()


if __name__ == "__main__":
    start_server("127.0.0.1", 12345)
