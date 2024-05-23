import unittest

import QUIC_Client
from QUIC_Client import send_message

class TestSendMessage(unittest.TestCase):
    def test_send_message(self):
        message = QUIC_Client.send_message("127.0.0.1", 12345)
        self.assertEqual(message, "ivan")


if __name__ == '__main__':
    unittest.main()