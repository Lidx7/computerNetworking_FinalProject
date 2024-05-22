import string
class LargePacket:
    id = ""
    type = ""
    def __init__(self, packet_id, packet_type):
        self.id = packet_id
        self.type = packet_type

    def _str_(self):
        return f"Packet ID: {self.id}, Packet Type: {self.type}"

    def set_id(self, new_id):
        self.id = new_id

    def set_type(self, new_type):
        self.type = new_type

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

def turn_toString(LargePacket):
    return str(LargePacket.get_id()) + "," + str(LargePacket.get_type())

def turn_backString(a):
    substring = a.split(',')
    return substring