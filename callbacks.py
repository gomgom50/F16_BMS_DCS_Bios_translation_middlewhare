from dcs_bios_reader import ProtocolParser, StringBuffer, IntegerBuffer

class Callbacks:
    def __init__(self, parser, shared_data):
        self.parser = parser
        self.shared_data = shared_data
        self.setup_dcs_bios_callbacks()

    def setup_dcs_bios_callbacks(self):
        # Setup callbacks for DED data (example addresses)
        self.ded_line1 = StringBuffer(self.parser, 0x450a, 29, self.handle_ded_line1)  # Replace 0x1234 with actual address
        self.ded_line2 = StringBuffer(self.parser, 0x4528, 29, self.handle_ded_line2)  # Replace 0x1248 with actual address

    def handle_ded_line1(self, value):
        # put data into shared_data under DCS key then DED_line1 key
        self.shared_data["DCS"]["DED_line1"] = value



    def handle_ded_line2(self, value):

        self.shared_data["DCS"]["DED_line2"] = value
