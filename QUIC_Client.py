import socket
import string
import random
import QUIC_Packet


def send_message(server_ip, server_port):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address0 = (server_ip, server_port)

    try:
        ivan = QUIC_Packet.LargePacket("214797367", "SYN")
        # Send the message to the server
        client_socket.sendto(QUIC_Packet.turn_toString( ivan ) .encode(), (server_ip, server_port))
        print(f"Message sent to {server_ip}:{server_port}")

        # Receive the response from the server

        response, server_address = client_socket.recvfrom(1024)
        subString = QUIC_Packet.turn_backString(response.decode())
        if subString[0]  != "326065646":
            print("Invalid id")
        if subString[1] != "ACK":
            print("Invalid")

        sequance_number = 1
        for i in range(0, 5):
            if (sequance_number == 5):
                packet = QUIC_Packet.LargePacket(sequance_number, "terminate")
                client_socket.sendto(QUIC_Packet.turn_toString(packet).encode(), (server_ip, server_port))
                break
            packet1 = QUIC_Packet.smallPacket(str(sequance_number),"ivan")
            sequance_number+=1
            client_socket.sendto(QUIC_Packet.turn_toString1(packet1).encode(), (server_ip, server_port))


    finally:
        client_socket.close()


if __name__ == "__main__":
    send_message("127.0.0.1", 12345)
