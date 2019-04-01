"""
A file to parse the data received from the android app : IMU+GPS stream

We have access to a sensor called orientation which,
I think, already have the Kalman blending done by android.
So this is better than what I can do...

There are also some stats about the update rate.
"""
import asyncio
from collections import deque

ORIENTATION_SENSOR_ID = 81
ORIENTATION = (None, None)
TS_DIFF = deque([], maxlen=1000)


def parse_data(data):
    """ sensor id :
        * id 3: accel
        * id 4: gyr
        * id 5: mag
        * id 81: orientation
    """
    global ORIENTATION

    sensors = {}
    ts, *data = data
    s_id, x, y, z, *tail = data
    sensors[s_id] = (x, y, z)
    while tail:
        s_id, x, y, z, *tail = tail
        sensors[s_id] = (x, y, z)

    if ORIENTATION_SENSOR_ID in sensors:
        if ORIENTATION[0]:
            TS_DIFF.append((ts - ORIENTATION[0]))
            print(
                "average time between orientation update (seconds)",
                sum(TS_DIFF) / len(TS_DIFF),
            )
        ORIENTATION = ts, sensors[ORIENTATION_SENSOR_ID]
        print(ORIENTATION[0], ORIENTATION[1][0])


class UPDServer:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        values = [float(v) for v in message.split(",")]
        # print('Received %r from %s' % (message, addr))
        parse_data(values)


loop = asyncio.get_event_loop()
print("Starting UDP server")
# One protocol instance will be created to serve all client requests
listen = loop.create_datagram_endpoint(UPDServer, local_addr=("0.0.0.0", 5555))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
