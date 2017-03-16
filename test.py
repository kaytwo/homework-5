"""
Utility script for testing HW5 solutions under user set conditions.
"""
import time
import argparse
import subprocess
import hashlib
import pathlib
import sys
import homework5.utils

DESC = sys.modules[globals()['__name__']].__doc__
PARSER = argparse.ArgumentParser(description=DESC)
PARSER.add_argument('-p', '--port', type=int, default=9999,
                    help="The port to simulate the lossy wire on (defaults to "
                         "9999).")
PARSER.add_argument('-l', '--loss', type=float, default=0.0,
                    help="The percentage of packets to drop.")
PARSER.add_argument('-d', '--delay', type=float, default=0.0,
                    help="The number of seconds, as a float, to wait before "
                         "forwarding a packet on.")
PARSER.add_argument('-b', '--buffer', type=int, default=100000,
                    help="The size of the buffer to simulate.")
PARSER.add_argument('-v', '--verbose', action="store_true",
                    help="Enable extra verbose mode.")
PARSER.add_argument('-s', '--send', required=True,
                    help="The file to send over the wire.")
PARSER.add_argument('-r', '--receive', required=True,
                    help="The path to write the received file to.")
ARGS = PARSER.parse_args()

PYTHON_BINARY = sys.executable
SERVER_ARGS = [PYTHON_BINARY, "server.py"]

if ARGS.verbose:
    SERVER_ARGS.append("-v")

for AN_ARG in ("port", "loss", "delay", "buffer"):
    SERVER_ARGS.append("--" + AN_ARG)
    SERVER_ARGS.append(str(getattr(ARGS, AN_ARG)))

SUBPROCESS_KWARGS = {} # {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
print(SERVER_ARGS)
SERVER_PROCESS = subprocess.Popen(SERVER_ARGS, **SUBPROCESS_KWARGS)
print("Starting wire process: {}".format(SERVER_PROCESS.pid))
time.sleep(1)

RECEIVING_ARGS = [PYTHON_BINARY, "receiver.py",
                  "--port", str(ARGS.port),
                  "--file", ARGS.receive]
RECEIVING_PROCESS = subprocess.Popen(RECEIVING_ARGS, **SUBPROCESS_KWARGS)
print("Starting receiving process: {}".format(RECEIVING_PROCESS.pid))
time.sleep(1)

SENDER_ARGS = [PYTHON_BINARY, "sender.py",
               "--port", str(ARGS.port),
               "--file", ARGS.send]
INPUT_PATH = pathlib.Path(ARGS.send)
INPUT_LEN, INPUT_HASH = homework5.utils.file_summary(INPUT_PATH)
START_TIME = time.time()

print("Starting sending process: {}".format(SERVER_PROCESS.pid))
SENDING_RESULT = subprocess.run(SENDER_ARGS, **SUBPROCESS_KWARGS)

END_TIME = time.time()

# Sleep the delay time, to allow the buffer to drain.
time.sleep(ARGS.delay)
RECEIVING_PROCESS.terminate()
SERVER_PROCESS.terminate()

RECV_PATH = pathlib.Path(ARGS.receive)
RECV_LEN, RECV_HASH = homework5.utils.file_summary(RECV_PATH)

if RECV_HASH == INPUT_HASH:
    print("Success")
else:
    print("Incorrect")
print("===\n")

print("Input")
print("---")
print("File: {}\nLength: {}\nHash: {}".format(
    str(INPUT_PATH), INPUT_LEN, INPUT_HASH))

print("\nReceived")
print("---")
print("File: {}\nLength: {}\nHash: {}".format(
    str(RECV_PATH), RECV_LEN, RECV_HASH))

print("\nStats")
print("Time: {} secs\nRate: {}".format(END_TIME - START_TIME, "TBD"))
