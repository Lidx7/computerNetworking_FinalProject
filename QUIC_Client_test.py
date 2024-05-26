import unittest
from unittest.mock import patch, MagicMock
import socket
import QUIC_Packet
import QUIC_Client

class TestClient(unittest.TestCase):
    @patch('socket.socket')
    def test_send_message(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Mock the response from the server
        mock_socket_instance.recvfrom.return_value = (QUIC_Packet.turn_toString(QUIC_Packet.LargePacket("326065646", "ACK")).encode(), ("127.0.0.1", 12345))

        # Calculate the expected number of sendto calls
        num_data_packets = (QUIC_Client.file_size + QUIC_Client.packet_data_buffer - 1) // QUIC_Client.packet_data_buffer  # Round up to account for any partial buffer
        num_windows = (num_data_packets + QUIC_Client.window_size - 1) // QUIC_Client.window_size  # Round up to account for any partial window
        expected_sendto_calls = num_data_packets + num_windows + 2  # +2 for initial SYN and final terminate packets

        # Run the client function
        QUIC_Client.send_message("127.0.0.1", 12345)

        # Assertions to check if packets were sent correctly
        self.assertTrue(mock_socket_instance.sendto.called)
        self.assertTrue(mock_socket_instance.recvfrom.called)
        self.assertEqual(mock_socket_instance.sendto.call_count, expected_sendto_calls)

if __name__ == "__main__":
    unittest.main()
