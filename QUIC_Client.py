import socket
import string
import random
import QUIC_Packet
file_size = 2 * 1000 * 1000
sending_loop = file_size // 1000
window_size = 5
packet_data_buffer = 1000


def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()


def send_message(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 1

    file = generate_random_data(file_size)

    try:
        SYN_Packet = QUIC_Packet.LargePacket("214797367", "SYN") #TODO: change the packet id to something reasonable (cant be just a random id)
        client_socket.sendto(QUIC_Packet.turn_toString( SYN_Packet ) .encode(), (server_ip, server_port))
        print(f"Message sent to {server_ip}:{server_port}")

        response, server_address = client_socket.recvfrom(1024) #TODO: consider making 1024 a constatnt (and maybe even mke it bigger)
        subString = QUIC_Packet.turn_backString(response.decode())
        if subString[0] != "326065646":
            print("Invalid id")
            return
        if subString[1] != "ACK":
            print("Invalid")
            return

        for i in range(0, sending_loop):
            buffer_counter = 0
            if i == (sending_loop - 1):
                packet = QUIC_Packet.LargePacket(sequence_number, "terminate")
                client_socket.sendto(QUIC_Packet.turn_toString(packet).encode(), (server_ip, server_port))
                break

            for j in range(0, window_size):
                #TODO: change packet1's name. give it a meaningful name
                packet1 = QUIC_Packet.smallPacket(str(sequence_number), file[packet_data_buffer * buffer_counter :
                                                                             packet_data_buffer * (buffer_counter + 1)])
                                                                          # This iterates over the file using a buffer
                sequence_number += 1
                buffer_counter += 1
                client_socket.sendto(QUIC_Packet.turn_toString1(packet1).encode(), (server_ip, server_port))
            finish_sending = QUIC_Packet.LargePacket("214797367", "SYN")
            # Send the message to the server
            client_socket.sendto(QUIC_Packet.turn_toString(finish_sending).encode(), (server_ip, server_port))
            response, server_address = client_socket.recvfrom(1024)
            subString = QUIC_Packet.turn_backString(response.decode())

            if subString[1] == "terminate":
                if subString[0] == "326065646":
                    sequence_number = sequence_number - window_size

                else:
                    sequence_number = int(subString[0])
            if subString[1] == "ACK":
                print("ACK received")

    finally:
        client_socket.close()


if __name__ == "__main__":
    send_message("127.0.0.1", 12345)


