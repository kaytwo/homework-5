"""
HW5: Sending Script
Client that sends STDIN, over a simulated faulty network connection.
"""

import argparse
import homework5.wire
import time

PARSER = argparse.ArgumentParser(description="Client script for sending data "
                                             "over a faulty network "
                                             "connection.")
PARSER.add_argument("-p", "--port", type=int, default=9999,
                    help="The port to connect to the simulated network over.")
PARSER.add_argument("-f", "--file", required=True,
                    help="The file to send over the simulated network.")
ARGS = PARSER.parse_args()

DATA = open(ARGS.file, 'rb').read()
DATA_LEN = len(DATA)

CHUNK_SIZE = homework5.MAX_PACKET
SOC = homework5.wire.bad_socket(ARGS.port)

CHUNK_OFFSETS = range(0, DATA_LEN, CHUNK_SIZE)
for CHUNK in [DATA[i:i + CHUNK_SIZE] for i in CHUNK_OFFSETS]:
    SOC.send(CHUNK)
    time.sleep(.5)

SOC.close()
