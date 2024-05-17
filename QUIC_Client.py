import asyncio
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

class TestClient(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            print("Handshake completed")
            self._quic.send_stream_data(0, b"Hello, QUIC!")
        elif isinstance(event, StreamDataReceived):
            print(f"Received: {event.data}")
            self._quic.close()

async def run():
    configuration = QuicConfiguration(is_client=True)
    async with connect("localhost", 4433, configuration=configuration, create_protocol=TestClient) as protocol:
        await protocol._quic.wait_closed()

if __name__ == "__main__":
    asyncio.run(run())
