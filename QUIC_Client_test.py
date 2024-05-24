import unittest
from unittest.mock import patch, call
from QUIC_Client import send_message


class TestSendMessage(unittest.TestCase):
    @patch('QUIC_Client.socket.socket')
    def test_send_message_ack(self, mock_socket):
        # Mock the socket.socket class and its methods
        mock_socket_instance = mock_socket.return_value
        # Mock the recvfrom method to return a tuple (response, address)
        mock_socket_instance.recvfrom.return_value = (
        b'{"id": "326065646", "type": "ACK"}', ("server_ip", "server_port"))

        # Call send_message function
        send_message("127.0.0.1", 12345)

        # Define the expected calls
        expected_calls = [
            call(b'214797367,SYN,LargePacket', ('127.0.0.1', 12345)),
             call(b'ivan,1,smallPacket', ('127.0.0.1', 12345)),
             call(b'ivan,2,smallPacket', ('127.0.0.1', 12345)),
             call(b'ivan,3,smallPacket', ('127.0.0.1', 12345)),
             call(b'ivan,4,smallPacket', ('127.0.0.1', 12345)),
             call(b'5,terminate,LargePacket', ('127.0.0.1', 12345))
        ]

        # Get the actual calls
        actual_calls = mock_socket_instance.sendto.call_args_list

        # Assert that the expected calls match the actual calls
        self.assertEqual(expected_calls, actual_calls)


if __name__ == '__main__':
    unittest.main()
