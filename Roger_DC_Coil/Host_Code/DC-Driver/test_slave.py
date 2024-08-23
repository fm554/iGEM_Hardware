import asyncio
import serial_asyncio
import serial

class SerialSimulatedSlave(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.buffer = b''
        self.peername = transport.get_extra_info('peername')
        print(f'Connection made with {self.peername}')

    def data_received(self, data):
        self.buffer += data
        if b'\n' in self.buffer:
            lines = self.buffer.split(b'\n')
            for line in lines[:-1]:
                self.handle_message(line.decode().strip())
            self.buffer = lines[-1]

    def handle_message(self, message):
        print(f'Received: {message}')
        if message == 'PING':
            self.transport.write(b'PONG\n')
            print('Sent: PONG')

    def connection_lost(self, exc):
        print('Connection lost')
        asyncio.get_event_loop().stop()

async def start_server(loop, port, baudrate):
    try:
        server = await serial_asyncio.create_serial_connection(
            loop, SerialSimulatedSlave, port, baudrate
        )
        print(f'Server running on {port}')
    except serial.SerialException as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

if __name__ == '__main__':
    port = 'COM2'  # Adjust to the suitable virtual COM port
    baudrate = 9600

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server(loop, port, baudrate))
        loop.run_forever()
    except KeyboardInterrupt:
        print('Simulation stopped.')
    finally:
        loop.close()
