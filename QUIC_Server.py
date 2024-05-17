import asyncio
import logging
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio.server import QuicServer
from aioquic.asyncio.ssl import create_self_signed_cert # TODO: fix this import problem or find a way to replace it
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

# Configure logging
logging.basicConfig(level=logging.INFO)


class EchoQuicProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            print(f"Handshake completed with {event.session_resumed}")
        elif isinstance(event, StreamDataReceived):
            print(f"Data received on stream {event.stream_id}: {event.data}")
            self._quic.send_stream_data(event.stream_id, event.data)
            self._quic.send_stream_data(event.stream_id, b"", end_stream=True)


async def run():
    # Generate a self-signed certificate
    cert, key = create_self_signed_cert()

    # QUIC configuration
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=cert, keyfile=key)

    # Create the QUIC server
    server = await QuicServer.create(
        host='127.0.0.1',
        port=4433,
        configuration=configuration,
        create_protocol=EchoQuicProtocol,
    )

    print("QUIC server running on 127.0.0.1:4433")

    try:
        await asyncio.Future()  # Run forever
    finally:
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(run())
