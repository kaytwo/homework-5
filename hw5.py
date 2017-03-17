"""
Where solution code to HW5 should be written.  No other files should
be modified.

You can import the following additional modules.  No other modules are allowed
for this assignment.
"""

import socket
import io
import time
import homework5

def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Naive implementation where we chunk the data to be sent into
    # packets as large as the network will allow, and then send them
    # over the network, pausing half a second between sends to let the
    # network "rest" :)
    chunk_size = homework5.MAX_PACKET
    offsets = range(0, len(data), homework5.MAX_PACKET)
    for chunk in [data[i:i + chunk_size] for i in offsets]:
        sock.send(chunk)
        time.sleep(.1)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """

    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.
    num_bytes = 0
    while True:
        data = sock.recv(homework5.MAX_PACKET)
        if not data:
            break
        dest.write(data)
        num_bytes += len(data)
        dest.flush()
    return num_bytes

