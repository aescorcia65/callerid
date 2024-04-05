#call_listener.py
import csv
import re # Used for parsing parts of CallerID.com records
import socket

UDP_IP = "0.0.0.0"  # listen on all available network interfaces
UDP_PORT = 3520  # choose a port number that matches the device's configuration
CSV_FILE = "calls.csv"  # name of the CSV file to save the data to
FULL_CALL_LOG = "full_call_log.csv"
NON_DETAILED_PATTERN = ".*(\d\d) ([IO]) ([ESB]) (\d{4}) ([GB]) (.)(\d) (\d\d/\d\d \d\d:\d\d [AP]M) (.{14})(.{15})"
DETAILED_PATTERN = ".*(\d\d) ([NFR]) {13}(\d\d/\d\d \d\d:\d\d:\d\d)"
# TAKE INPUT DATA AND PARSE PARTS
def parse_packet(packet):

    # Decode packet from bytes to readable text
    packet = packet.decode("utf-8", 'backslashreplace')

    non_detailed_match = re.search(NON_DETAILED_PATTERN, packet)

    # Parsed non_detailed variables for use in program
    pLineNumber = ""
    pDateTime = ""
    pNumber = ""
    pName = ""

    # If call is a non-deatiled packet
    if non_detailed_match:

        # Parse variables
        pLineNumber = non_detailed_match.group(1)
        pDateTime = non_detailed_match.group(8)
        pNumber = non_detailed_match.group(9)
        pName = non_detailed_match.group(10)

        # For testing purposes - check variables
        print("Call Record ----------\n")
        print("Line: " + pLineNumber + "\n")
        print("DateTime: " + pDateTime + "\n")
        print("Number: " + pNumber + "\n")
        print("Name: " + pName + "\n")
        print("----------------------\n")

        call_data = {
        "timestamp": pDateTime,
        "number": pNumber,
        "name": pName
    }

    # write the Csv object to the file
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([call_data['number'], call_data['timestamp'],call_data['name']])

    with open(FULL_CALL_LOG, "a", newline="") as f2:
        writer = csv.writer(f2)
        writer.writerow([call_data['number'], call_data['timestamp'],call_data['name']])

# create a UDP socket and bind it to the specified IP address and port number
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets on port {}...".format(UDP_PORT))

# # create a CSV file and write a header row
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number", "timestamp", "name"])


# # continuously receive UDP packets and write their contents to the CSV file
while True:
    data, addr = sock.recvfrom(1024)  # receive up to 1024 bytes of data
    parse_packet(data)
