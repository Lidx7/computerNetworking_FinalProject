import unittest
from QUIC_Server import start_server  # Import the function that starts the server

class TestStartServer(unittest.TestCase):
    def test_start_server(self):
        start = start_server("127.0.0.1", 12345)

        self.assertTrue(start)

if __name__ == '__main__':
    unittest.main()
