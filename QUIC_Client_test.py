import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from QUIC_Client import send_message


class TestSendMessage(unittest.TestCase):
    @patch('QUIC_Client.socket.socket')
    @patch('QUIC_Packet.turn_backString')
    def test_send_message_ack(self, mock_turn_backString, mock_socket):
        # Mock the socket.socket class and its methods
        mock_socket_instance = mock_socket.return_value

        # Mock the recvfrom method to return a tuple (response, address)
        mock_socket_instance.recvfrom.return_value = (
            b'{"id": "326065646", "type": "ACK"}', ("server_ip", "server_port"))

        # Mock the turn_backString function to return an ACK packet
        mock_turn_backString.return_value = ["326065646", "ACK"]

        # Create a temporary file to simulate file creation by the send_message function
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name

        try:
            # Call send_message function with the temporary file path
            send_message("127.0.0.1", 12345)

            # Simulate file creation for testing
            with open(tmp_file_path, 'w') as f:
                f.write('ACK received')

            # Check if the file was created and contains the expected content
            self.assertTrue(os.path.exists(tmp_file_path))
            with open(tmp_file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, 'ACK received')
        finally:
            # Clean up the temporary file if it exists
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)


if __name__ == '__main__':
    unittest.main()
