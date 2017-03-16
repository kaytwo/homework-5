"""
HW5: Receiving Script
Client that receives data over a simulated slow socket, and writes the results
to STDOUT.
"""

import argparse
import sys
import homework5.wire

PARSER = argparse.ArgumentParser(description="Client script for sending data "
                                             "over a faulty network "
                                             "connection.")
PARSER.add_argument("-p", "--port", type=int, default=9999,
                    help="The port to connect to the simulated network over.")
PARSER.add_argument("-f", "--file", type=str,
                    help="The path to write the data recorded over the buffer "
                         "to (default=STDOUT).")
ARGS = PARSER.parse_args()

OUTPUT = open(ARGS.file, 'wb') if ARGS.file else sys.stdout.buffer

SOC = homework5.wire.bad_socket(ARGS.port)

while True:
    DATA = SOC.recv(homework5.MAX_PACKET)
    if not DATA:
        break
    OUTPUT.write(DATA)
    OUTPUT.flush()

SOC.close()
OUTPUT.close()
