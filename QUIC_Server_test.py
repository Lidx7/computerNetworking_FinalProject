import unittest
from unittest.mock import patch, MagicMock
import socket
import QUIC_Packet
import QUIC_Server

class TestServer(unittest.TestCase):
    @patch('socket.socket')
    def test_start_server(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Mock the client's packets
        mock_socket_instance.recvfrom.side_effect = [
            (QUIC_Packet.turn_toString(QUIC_Packet.LargePacket("214797367", "SYN")).encode(), ("127.0.0.1", 12345)),
            (QUIC_Packet.turn_toString1(QUIC_Packet.smallPacket("1", "data1")).encode(), ("127.0.0.1", 12345)),
            (QUIC_Packet.turn_toString(QUIC_Packet.LargePacket("214797367", "terminate")).encode(), ("127.0.0.1", 12345))
        ]

        # Run the server function
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            QUIC_Server.start_server("127.0.0.1", 12345)

            # Assertions to check if packets were sent and received correctly
            self.assertTrue(mock_socket_instance.sendto.called)
            self.assertTrue(mock_socket_instance.recvfrom.called)

            # Print out the call arguments to understand what is being sent
            for call in mock_socket_instance.sendto.call_args_list:
                print(call)

            # Expected: 1 sendto calls (ACK for SYN)
            self.assertEqual(mock_socket_instance.sendto.call_count, 1)

if __name__ == "__main__":
    unittest.main()
