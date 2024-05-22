import string
class LargePacket:
    id = ""
    type = ""

    def __init__(self, packet_id, packet_type):
        self.id = packet_id
        self.type = packet_type
        self.packet_type = "LargePacket"

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
class smallPacket:
    data = " "
    sequence_Number=0

    def __init__(self,sequence_Number,data):
        self.sequence_Number = sequence_Number
        self.data =data
        self.packet_type = "smallPacket"

    def _str_(self):
        return f"Packet sequance number: {self.sequence_Number}, Packet data: {self.data}"

    def set_data(self, new_id):
        self.data = new_id

    def set_number(self, new_type):
        self.sequence_Number = new_type

    def get_number(self):
        return self.sequence_Number

    def get_data(self):
        return self.data




def turn_toString(LargePacket):
    return str(LargePacket.get_id()) + "," + str(LargePacket.get_type()) +",LargePacket"
def turn_toString1(smallPacket):
    return str(smallPacket.get_data()) + "," + str(smallPacket.get_number()) +",smallPacket"
def turn_backString(a):
    substring = a.split(',')
    return substring