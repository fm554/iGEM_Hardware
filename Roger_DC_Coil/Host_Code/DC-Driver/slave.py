import asyncio
import serial_asyncio
import serial
import random

class Arduino_Magnet(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        device_name = f"Magnet{random.randint(100, 999)}"
        #print(f"Device name: {device_name}")
        self.name = device_name
        
        self.buffer = b''
        #self.peername = transport.get_extra_info('peername')
        #print(f'Connection made with {self.peername}')

    def Serial_pingpong(self, message):
        if message.startswith('HEAD'):
            params = message.split(";")
        else:
            return None
        if len(params) == 6:
            on = int(params[0])
            mode = int(params[1])
            pole = int(params[2])
            amplitude = int(float(params[3]))
            freq = int(float(params[4]))
            checksum = int(params[5])
            calculated_checksum = (on + mode + pole + amplitude + freq) % 11
            if calculated_checksum == checksum:
                self.transport.write(f'{calculated_checksum}\n')
                return [on, mode, pole, amplitude, freq]
            else:
                return "Checksum error"

    def report(self, message):
        self.transport.write(message.encode())

    def connection_lost(self, exc):
        print('Connection lost')
        self.transport.loop.stop()

async def main():
    loop = asyncio.get_running_loop()
    port = 'CNCB0'  # Adjust to a suitable virtual COM port
    baudrate = 9600

    try:
        server = await serial_asyncio.create_serial_connection(
            loop, SerialSimulatedSlave, port, baudrate
        )
        print(f'Server running on {port}')
    except serial.SerialException as e:
        print(f"Error: {e}")
        return

    try:
        await loop.run_forever()
    except KeyboardInterrupt:
        print('Simulation stopped.')

if __name__ == '__main__':
    asyncio.run(main())
