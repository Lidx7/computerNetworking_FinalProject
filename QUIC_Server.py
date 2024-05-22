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
    packet =QUIC_Packet.LargePacket(326065646, "ACK")
    if substring[0] == "214797367":
        if substring[1]=="SYN":
            server_socket.sendto(QUIC_Packet.turn_toString(packet).encode(),server_address)
    else:
        print("Invalid id")

    while True:
        data, address =server_socket.recvfrom(1024)
        substring1 = QUIC_Packet.turn_backString(data.decode())
        if substring1[2] == "LargePacket":
            if substring1[1] == "terminate":
                break
        print(f"{substring1[0]} , {substring1[1]}")
    server_socket.close()


if __name__ == "__main__":
    start_server("127.0.0.1", 12345)
