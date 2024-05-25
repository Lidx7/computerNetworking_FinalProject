import socket
import random
import string
import QUIC_Packet
file_size = 2 * 1000 * 1000
sending_loop = file_size // 1000
window_size = 5
packet_data_buffer = 1000
# def generate_random_data(size):
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()
def start_server(ip, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    stop_it=True
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
        return
    sequance_number = 1
    while True:
        response, server_address = server_socket.recvfrom(1024)
        # Handle the response if needed
        substring1 = QUIC_Packet.turn_backString(response.decode())
        if substring1[2]=="LargePacket":
            if substring1[1]=="SYN":
                if sequance_number%5 -1 != 0  :
                    print(f"something went wrong,{sequance_number-1} was missing")
                    bad_packet_sending = QUIC_Packet.LargePacket("326065646", "terminate")
                    server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
                    stop_it=True
                    sequance_number-=4



            if substring1[1] == "terminate":
                break
            continue
       

        if substring1[2]=="smallPacket" and sequance_number == int(substring1[1]):
            stop_it=True
        if int(substring1[1]) != sequance_number and stop_it:
            print(sequance_number)
            stop_it=False
            if sequance_number%5==0:
                missing_five=sequance_number-4
            else:
                missing_five=sequance_number-sequance_number%5 +1
                print(missing_five)
            bad_packet_sending = QUIC_Packet.LargePacket(str(missing_five), "terminate")
            server_socket.sendto(QUIC_Packet.turn_toString(bad_packet_sending).encode(), server_address)
            sequance_number= missing_five
            continue
        if int(substring1[1])%5==0:
            if  stop_it:
                good_packet_sending = QUIC_Packet.LargePacket(326065646, "ACK")
                server_socket.sendto(QUIC_Packet.turn_toString(good_packet_sending).encode(),server_address)
        if stop_it:
            sequance_number = sequance_number+1
            print(f" packet number {substring1[1]} , the data :{substring1[0]}")
    server_socket.close()


if __name__ == "__main__":
    start_server("127.0.0.1",12345)
