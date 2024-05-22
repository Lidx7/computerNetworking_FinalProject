import struct
import pickle

class Packet:
    def __init__(self, packet_number, payload):
        self.packet_number = packet_number
        self.payload = payload
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        # Simulated checksum calculation
        return sum([ord(char) for char in self.payload])

    def quicEncode(packet):
        # For simplicity, let's assume the header is a fixed size (e.g., 8 bytes) and     payload is variable size.
        header_format = '8s'  # 8 bytes string for header
        payload_format = f'{len(packet.payload)}s'  # Variable length string for          payload

        # Combine the formats
        packet_format = header_format + payload_format

        # Pack the data
        encoded_packet = struct.pack(packet_format, packet.header.encode(), packet.payload.encode())
        return encoded_packet
    @classmethod
    def quicDecode(encoded_packet):
        # For simplicity, let's assume the header is always 8 bytes
        header_format = '8s'
        header_size = struct.calcsize(header_format)

        # Extract the header
        header = struct.unpack(header_format, encoded_packet[:header_size])[0].decode().strip('\x00')

        # Extract the payload
        payload = encoded_packet[header_size:].decode()

        return QuicPacket(header, payload)
