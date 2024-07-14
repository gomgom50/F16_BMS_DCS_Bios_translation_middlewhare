# Define a mapping for special control characters
CONTROL_CHAR_MAPPING = {
    b'\x00': '',  # Null character
    b'\x02': '[*]',  # Special character: star with a solid square
    # Add more mappings as necessary
}

class DEDHandler:
    def __init__(self, arduino_connection, mode, shared_data, middleware):
        self.arduino_connection = arduino_connection
        self.mode = mode
        self.shared_data = shared_data
        self.last_message = None  # To store the last sent message
        self.shared_data["DCS"]["DED_line1"] = ""
        self.shared_data["DCS"]["DED_line2"] = ""
        self.middleware = middleware

    def process_data(self):
        if self.mode == 'DCS':
            # Handle DCS data
            ded_line1 = self.shared_data["DCS"]["DED_line1"]
            ded_line2 = self.shared_data["DCS"]["DED_line2"]

            # Ensure the lines are correctly stripped and combined with a delimiter
            message = f"{ded_line1.strip()},{ded_line2.strip()}"

        elif self.mode == 'BMS':
            # Extract DED lines from shared data
            flight_data = self.shared_data["BMS_flightdata"]
            ded_lines = self.extract_ded_lines(flight_data)
            ded_line1 = ded_lines[0] if len(ded_lines) > 0 else ""
            ded_line2 = ded_lines[1] if len(ded_lines) > 1 else ""


            # Ensure the lines are correctly stripped and combined with a delimiter
            message = f"{ded_line1.strip()},{ded_line2.strip()}"

        # Send the message to the Arduino only if it has changed
        if message != self.last_message:
            self.last_message = message
            print(f"Sending message to Arduino: '{message}'")
            self.arduino_connection.send_data(message)

        # Handle button press (assume Arduino sends "Button pressed" when the button is pressed)
        line = self.arduino_connection.read_data()
        # if message is None return
        if line is None:
            return

        if self.mode == 'DCS':
            self.middleware.send_message_to_dcs(line)
        elif self.mode == 'BMS':
            self.middleware.bms_handler.send_key(line)




    def decode_character(self, b):
        b_int = ord(b) if isinstance(b, bytes) else b
        if 32 <= b_int <= 126:  # Printable ASCII range
            return chr(b_int)
        return CONTROL_CHAR_MAPPING.get(bytes([b_int]), f'\\x{b_int:02x}')  # Map control characters or show as hex

    def extract_ded_lines(self, flight_data):
        ded_lines = []
        for i in range(5):  # There are 5 lines
            line_bytes = getattr(flight_data, "DEDLines")[i]
            line = ''.join(self.decode_character(b) for b in line_bytes).strip()  # Decode each line from bytes to string and strip any extra spaces
            ded_lines.append(line)
        return ded_lines

