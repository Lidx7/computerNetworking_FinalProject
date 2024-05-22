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

    def quicEncode(self):
        # Serialize the packet object into bytes using pickle
        return pickle.dumps(self)

    def quicDecode(cls, data):
        # Deserialize bytes into a QUICPacket object using pickle
        try:
            packet = pickle.loads(data)
            if packet.checksum != packet.calculate_checksum():
                raise ValueError("Checksum does not match, packet may be corrupted.")
            return packet
        except (pickle.PickleError, ValueError) as e:
            print(f"Error decoding packet: {e}")
            return None

