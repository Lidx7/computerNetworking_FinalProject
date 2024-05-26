import socket
import time
from _socket import timeout
import QUIC_Packet
from datetime import datetime

packet_id1 = "214797367"
packet_id2 = "326065646"
socket_num = 1024
window_size = 5
time_sleeping = 0.01
time_out = 0.5

def start_server(ip, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"UDP server listening on {ip}:{port}")

    response, server_address = server_socket.recvfrom(socket_num)
    DataDivider = QUIC_Packet.turn_backString(response.decode())
    start_time = datetime.now()
    packet = QUIC_Packet.LargePacket(packet_id2, "ACK")
    file = open("file_sent", "w+")
    stop_it = True

    if DataDivider[0] == packet_id1:
        if DataDivider[1] == "SYN":
            server_socket.sendto(QUIC_Packet.turn_toString(packet).encode(), server_address)
    else:
        print("Invalid id")
        return
    sequence_number = 1
    five_packets = ""
    server_socket.settimeout(time_out)
    send_ack = False
    try:
        while True:
            try:
                data, address = server_socket.recvfrom(socket_num)
                print(f"Received packet: {data} from {address}")  # Debugging statement
            except timeout:
                if send_ack:
                    good_packet_sending = QUIC_Packet.LargePacket(packet_id2, "ACK")
                    server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(), server_address)
                    send_ack = False
                continue
            send_ack = False
            DataDivider = QUIC_Packet.turn_backString(data.decode())

            if DataDivider[2] == "LargePacket":
                if DataDivider[1] == "SYN":
                    if sequence_number % window_size - 1 != 0:
                        print(f"something went wrong, {sequence_number} was missing")
                        bad_packet_sending = QUIC_Packet.LargePacket(packet_id2, "terminate")
                        server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
                        stop_it = True
                        sequence_number -= 4
                        continue

                if "terminate" in DataDivider[1]:
                    break
                continue

            if DataDivider[2] == "smallPacket" and sequence_number == int(DataDivider[1]):
                stop_it = True
            if not stop_it:
                five_packets = ""

            if int(DataDivider[1]) != sequence_number and stop_it:
                print(sequence_number)
                if sequence_number % window_size == 0:
                    missing_five = sequence_number - 4
                else:
                    missing_five = sequence_number - sequence_number % window_size + 1
                    print(missing_five)
                bad_packet_sending = QUIC_Packet.LargePacket(str(missing_five), "terminate")
                server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
                stop_it = False
                sequence_number = missing_five
                print(f"{DataDivider[1]} did not arrive")
                time.sleep(time_sleeping)
                continue

            if int(DataDivider[1]) % window_size == 0:
                if stop_it:
                    good_packet_sending = QUIC_Packet.LargePacket(packet_id2, "ACK")
                    server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(), server_address)
                    time.sleep(time_sleeping)
                    print(f"Writing packets to file: {five_packets}")  # Debugging statement
                    file.write(five_packets)
                    file.flush()  # Ensure data is written to file
                    send_ack = True
            if stop_it:
                sequence_number = sequence_number + 1
                five_packets += DataDivider[0]
                print(f" packet number {DataDivider[1]} , the data :{DataDivider[0]}")

    finally:
        server_socket.close()
        file.close()
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))


if __name__ == "__main__":
    start_server("127.0.0.1", 12345)
