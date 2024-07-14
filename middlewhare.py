import serial
import time
import json
from threading import Thread, Event
import socket
import sys
import struct
import errno

from dcs_bios_reader import ProtocolParser
from falcon_bms_reader import read_shared_memory, FlightData, FlightData2, IntellivibeData, read_shared_memory_strings
from callbacks import Callbacks
from ded_handler import DEDHandler
from BMSKeyHandler import FalconBMSHandler


class ArduinoConnection:
    def __init__(self, name, com_port, baud_rate):
        self.name = name
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_conn = serial.Serial(
            port=com_port,
            baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None,
            rtscts=False,
            dsrdtr=False
        )

    def send_data(self, data):
        self.serial_conn.write(data.encode() + b'\n')


    def read_data(self):
        if self.serial_conn.in_waiting > 0:
            line = self.serial_conn.readline().decode('utf-8').strip()
            print(f"Received from {self.name}: {line}")
            return line
        return None


class Middleware:
    def __init__(self, config_path, mode):
        self.load_config(config_path)
        self.mode = mode
        self.arduino_connections = {
            arduino["name"]: ArduinoConnection(arduino["name"], arduino["com_port"], arduino["baud_rate"]) for arduino
            in self.config["arduinos"]}
        self.shared_data = {}
        self.shared_data["BMS_flightdata"] = None
        self.shared_data["BMS_flightdata2"] = None
        self.shared_data["BMS_intellivibe"] = None
        self.shared_data["BMS_strings"] = None
        self.shared_data["DCS"] = {}
        self.parser = ProtocolParser()
        self.dcs_thread = None
        self.stop_event = Event()
        self.socket = None
        self.bms_handler = None

        if self.mode == 'DCS':
            self.callbacks = Callbacks(self.parser, self.shared_data)
            self.start_dcs_thread()
        elif self.mode == 'BMS':
            self.bms_handler = FalconBMSHandler()


        # Initialize handlers for different components
        self.ded_handler = DEDHandler(self.arduino_connections["DED"], self.mode, self.shared_data, self)

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def send_to_arduino(self, name, data):
        if name in self.arduino_connections:
            self.arduino_connections[name].send_data(data)

    def read_falcon_data(self):
        flightdata = read_shared_memory(FlightData)
        flightdata2 = read_shared_memory(FlightData2)
        strings = read_shared_memory_strings()
        # put data in shared_data
        self.shared_data["BMS_flightdata"] = flightdata
        self.shared_data["BMS_flightdata2"] = flightdata2
        self.shared_data["BMS_strings"] = strings


    def run(self):
        while True:
            if self.mode == 'DCS':
                # Process data using the DED handler
                self.ded_handler.process_data()
                #self.send_message_to_dcs("MMC_PWR_SW", 1)
            elif self.mode == 'BMS':
                self.read_falcon_data()
                # Process BMS data using the DED handler
                self.ded_handler.process_data()


    def start_dcs_thread(self):
        self.stop_event.clear()
        self.dcs_thread = Thread(target=self.start_dcs_reader)
        self.dcs_thread.start()

    def stop_dcs_thread(self):
        if self.dcs_thread:
            self.stop_event.set()
            self.dcs_thread.join()
            self.dcs_thread = None

    import struct
    import errno

    def start_dcs_reader(self):
        CONNECTION = {
            "type": "UDP",
            "multicast_group": "239.255.50.10",
            "port": 5010
        }

        if CONNECTION["type"] == "UDP":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", CONNECTION["port"]))

            # Join multicast group
            mreq = struct.pack("4sl", socket.inet_aton(CONNECTION["multicast_group"]), socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            s.settimeout(0)  # Set the socket to non-blocking mode

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("DCS reader started")
        print("Listening on port", CONNECTION["port"])
        print(f"Joined multicast group {CONNECTION['multicast_group']}")

        while not self.stop_event.is_set():
            try:
                data, addr = s.recvfrom(8192)
                if data:
                    for c in data:
                        self.parser.processByte(bytes([c]))  # Ensure each byte is passed correctly
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    # These are expected errors for non-blocking sockets when no data is available
                    continue
                else:
                    print("Socket error:", e)
            except Exception as e:
                print("Unexpected error:", e)

    def send_message_to_dcs(self, message):
        udp_receiver_ip = '127.0.0.1'
        port = 7778

        try:
            self.socket.sendto(bytes(str(message) + '\n', "utf-8"), (udp_receiver_ip, port))
        except Exception as e:
            print(f"Error sending message to DCS: {e}")


    def console_test(self):
        while True:
            try:
                user_input = input("Enter message to send to DCS (or 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    break
                self.send_message_to_dcs(user_input)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python middleware.py <config_path> <mode>")
        print("mode: DCS or BMS")
        sys.exit(1)

    config_path = sys.argv[1]
    mode = sys.argv[2]

    if mode not in ['DCS', 'BMS']:
        print("Invalid mode. Use 'DCS' or 'BMS'.")
        sys.exit(1)

    middleware = Middleware(config_path, mode)

    # Run the main middleware loop
    middleware.run()
