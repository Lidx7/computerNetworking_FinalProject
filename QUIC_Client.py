import socket
import string
import random
from _socket import timeout

import QUIC_Packet
import time
from datetime import datetime

packet_id1 = "214797367"
packet_id2 = "326065646"
socket_num = 1024
window_size = 5
time_out = 0.5
file_size = 5 * 1000 * 100
packet_data_buffer = 1000
time_sleeping = 0.01


def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()


def send_message(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 1
    buffer_counter = 0
    file = generate_random_data(file_size)
    start_time = datetime.now()

    try:
        SYN_Packet = QUIC_Packet.LargePacket(packet_id1, "SYN")
        client_socket.sendto(QUIC_Packet.turn_toString( SYN_Packet ) .encode(), (server_ip, server_port))
        print(f"Message sent to {server_ip}:{server_port}")

        response, server_address = client_socket.recvfrom(socket_num)
        DataDivider = QUIC_Packet.turn_backString(response.decode())
        if DataDivider[0] != packet_id2:
            print("Invalid id")
            return
        if DataDivider[1] != "ACK":
            print("Invalid")
            return


        client_socket.settimeout(time_out)

        while file[(packet_data_buffer * buffer_counter) : (packet_data_buffer * (buffer_counter + 1))] != b'':

            while True:
                for j in range(0, window_size):
                    #packet1's name changed to packetiterate
                    packetiterate = QUIC_Packet.smallPacket(str(sequence_number), file[(packet_data_buffer * buffer_counter) :
                                                                                 (packet_data_buffer * (buffer_counter + 1))])
                                                                              # This iterates over the file using a buffer
                    client_socket.sendto(QUIC_Packet.turn_toString1(packetiterate).encode(), (server_ip, server_port))
                    time.sleep(time_sleeping)
                    sequence_number += 1
                    buffer_counter += 1

                finish_sending = QUIC_Packet.LargePacket(packet_id1, "ACK") #changed to ACK

                client_socket.sendto(QUIC_Packet.turn_toString(finish_sending).encode(), (server_ip, server_port))
                try:
                    response, server_address = client_socket.recvfrom(socket_num)
                except timeout:

                    continue

                DataDivider = QUIC_Packet.turn_backString(response.decode())

                if DataDivider[1] == "terminate":
                    if DataDivider[0] == packet_id2:
                        sequence_number = sequence_number - window_size
                        break

                    else:
                        sequence_number = int(DataDivider[0])
                if DataDivider[1] == "ACK":
                    print("ACK received")
                    break
        packet = QUIC_Packet.LargePacket(sequence_number, "terminate")
        client_socket.sendto(QUIC_Packet.turn_toString(packet).encode(), (server_ip, server_port))

    finally:
        client_socket.close()
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))


if __name__ == "__main__":
    send_message("127.0.0.1", 12345)


