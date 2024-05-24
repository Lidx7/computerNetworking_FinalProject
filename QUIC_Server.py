import socket
import random
import string
import QUIC_Packet
window_size = 5


def start_server(ip, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"UDP server listening on {ip}:{port}")

    response, server_address = server_socket.recvfrom(1024) #TODO: consider making 1024 a constatnt (and maybe even mke it bigger)
    substring = QUIC_Packet.turn_backString(response.decode())
    # TODO: change the packet id to something reasonable (cant be just a random id, but it need to have some logic behind the choice)
    packet =QUIC_Packet.LargePacket(326065646, "ACK")
    file = open("file_sent", "w+")

    if substring[0] == "214797367":
        if substring[1] == "SYN":
            server_socket.sendto(QUIC_Packet.turn_toString(packet).encode(),server_address)
    else:
        print("Invalid id")
        return
    sequence_number = 1
    while True:
        data, address =server_socket.recvfrom(1024)
        substring1 = QUIC_Packet.turn_backString(data.decode()) #TODO: change substring1's name and give it a meaningful name
        if substring1[2] == "LargePacket":
            if substring1[1] == "terminate":
                break

        if int(substring1[1]) != sequence_number:
            bad_packet_sending = QUIC_Packet.LargePacket(326065646, "terminate")
            server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
            sequence_number -= sequence_number%5
            print("{substring1[1]} does not arrived")
            continue
        if int(substring1[1])%window_size == 0:
            good_packet_sending = QUIC_Packet.LargePacket(326065646, "ACK")
            server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(),server_address)
        sequence_number += 1
        print(f" packet number {substring1[1]} , the data :{substring1[0]}")
        file.write(substring1[0])
    server_socket.close()
    file.close()


if __name__ == "__main__":
    start_server("127.0.0.1", 12345)
