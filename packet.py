import struct
import zlib


class QUICPacket:
    def __init__(self, packet_number, payload):
        self.packet_number = packet_number
        self.payload = payload
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        # Using zlib's adler32 for checksum calculation
        checksum = zlib.adler32(self.payload.encode('utf-8'))
        return checksum

    def serialize(self):
        # Serialize the packet data into bytes
        packet_number_bytes = struct.pack('!I', self.packet_number)
        checksum_bytes = struct.pack('!I', self.checksum)
        payload_bytes = self.payload.encode('utf-8')

        return packet_number_bytes + checksum_bytes + payload_bytes

    @classmethod
    def deserialize(cls, data):
        # Deserialize bytes into a QUICPacket object
        packet_number = struct.unpack('!I', data[:4])[0]
        checksum = struct.unpack('!I', data[4:8])[0]
        payload = data[8:].decode('utf-8')

        packet = cls(packet_number, payload)
        if packet.checksum != checksum:
            raise ValueError("Checksum does not match, packet may be corrupted.")

        return packet



# Example usage:
# packet = QUICPacket(1, "Hello, QUIC!")
# serialized_packet = packet.serialize()
# print(f"Serialized packet: {serialized_packet}")
#
# deserialized_packet = QUICPacket.deserialize(serialized_packet)
# print(
#     f"Deserialized packet - Packet Number: {deserialized_packet.packet_number}, Payload: {deserialized_packet.payload}, Checksum: {deserialized_packet.checksum}")
