import socket
import random
import string
import time
import QUIC_Packet
from datetime import datetime

window_size = 5


def start_server(ip, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    server_socket.settimeout(5)
    print(f"UDP server listening on {ip}:{port}")

    response, server_address = server_socket.recvfrom(1024) #TODO: consider making 1024 a constatnt (and maybe even mke it bigger)
    substring = QUIC_Packet.turn_backString(response.decode())
    start_time = datetime.now()
    # TODO: change the packet id to something reasonable (cant be just a random id, but it need to have some logic behind the choice)
    packet =QUIC_Packet.LargePacket(326065646, "ACK")
    file = open("file_sent", "w+")
    stop_it = True


    if substring[0] == "214797367":
        if substring[1] == "SYN":
            server_socket.sendto(QUIC_Packet.turn_toString(packet).encode(),server_address)
    else:
        print("Invalid id")
        return
    sequence_number = 1
    five_packets = ""
    try:
        while True:
            try:
                data, address = server_socket.recvfrom(1024)
            except socket.timeout:
                good_packet_sending = QUIC_Packet.LargePacket(326065646, "ACK")
                server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(), server_address)
                continue
            substring1 = QUIC_Packet.turn_backString(data.decode()) #TODO: change substring1's name and give it a meaningful name

            if substring1[2] == "LargePacket":
                if substring1[1]=="SYN":
                    if sequence_number % 5 - 1 != 0:
                        print(f"something went wrong,{sequence_number} was missing")
                        bad_packet_sending = QUIC_Packet.LargePacket("326065646", "terminate")
                        server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
                        stop_it = True
                        sequence_number -= 4
                        continue

                if "terminate" in substring1[1]:
                    break
                continue

            if substring1[2] == "smallPacket" and sequence_number == int(substring1[1]):
                stop_it = True
            if not stop_it:
                five_packets = ""

            if int(substring1[1]) != sequence_number and stop_it:
                print(sequence_number)
                if sequence_number % 5 == 0:
                    missing_five = sequence_number-4
                else:
                    missing_five = sequence_number-sequence_number % 5 + 1
                    print(missing_five)
                bad_packet_sending = QUIC_Packet.LargePacket(str(missing_five), "terminate")
                server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
                stop_it = False
                sequence_number = missing_five
                print(f"{substring1[1]} does not arrived")
                time.sleep(0.001)
                continue

            if int(substring1[1]) % window_size == 0:
                if stop_it:
                    good_packet_sending = QUIC_Packet.LargePacket(326065646, "ACK")
                    server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(), server_address)
                    time.sleep(0.001)
                    file.write(five_packets)
            if stop_it:
                sequence_number = sequence_number+1
                five_packets += substring1[0]
                print(f" packet number {substring1[1]} , the data :{substring1[0]}")

    finally:
        server_socket.close()
        file.close()
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))


if __name__ == "__main__":
    start_server("127.0.0.1", 12345)
