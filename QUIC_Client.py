import socket
import string
import random
import QUIC_Packet


def send_message(server_ip, server_port):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address0 = (server_ip, server_port)
    # cid_length = 16
    # cid_characters = string.ascii_letters + string.digits

    try:
        ivan = QUIC_Packet.LargePacket("214797367", "sinq")
        # Send the message to the server
        client_socket.sendto(QUIC_Packet.turn_toString( ivan ) .encode(), (server_ip, server_port))
        print(f"Message sent to {server_ip}:{server_port}")

        # Receive the response from the server

        response, server_address = client_socket.recvfrom(1024)
        subString = QUIC_Packet.turn_backString(response.decode())
        id = subString[0]
        print(id)
        type = subString[1]
        print(type)
    finally:
        client_socket.close()


if __name__ == "__main__":
    send_message("127.0.0.1", 12345)
