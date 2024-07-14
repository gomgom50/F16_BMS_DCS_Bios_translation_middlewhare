import keyboard
import time
import pyvjoy

class FalconBMSHandler:
    def __init__(self):
        self.key_mappings = self.load_keyfile('keyfile.txt')
        self.key_mappings = self.convert_keymap(self.key_mappings, self.hex_to_key)
        #print(keyboard._keyboard_event.canonical_names)
        #print(self.key_mappings)
        self.pot_mappings = {
            "ICP_HUD_BRT_KNB": pyvjoy.HID_USAGE_X,
        }
        self.joy = pyvjoy.VJoyDevice(1)  # Initialize vJoy device


    hex_to_key = {
        "0x2": '1',
        "0x3": '2',
        "0x4": '3',
        "0x5": '4',
        "0x6": '5',
        "0x7": '6',
        "0x8": '7',
        "0x9": '8',
        "0xa": '9',
        "0xb": '0',
        "0xc": 'minus',
        "0xd": 'equals',
        "0xe": 'backspace',
        "0x16": 'u',
        "0x17": 'i',
        "0x18": 'o',
        "0x19": 'p',
        "0x1a": 'left brace',
        "0x1b": 'right brace',
        "0x1e": 'a',
        "0x1f": 's',
        "0x20": 'd',
        "0x22": 'g',
        "0x23": 'h',
        "0x24": 'j',
        "0x25": 'k',
        "0x26": 'l',
        "0x27": 'semicolon',
        "0x28": 'apostrophe',
        "0x29": 'backquote',
        "0x2b": 'backslash',
        "0x2c": 'z',
        "0x2d": 'x',
        "0x2e": 'c',
        "0x2f": 'v',
        "0x30": 'b',
        "0x31": 'n',
        "0x32": 'm',
        "0x33": 'comma',
        "0x34": 'period',
        "0x35": 'slash',
        "0x37": 'keypad *',
        "0x39": 'spacebar',
        "0x3a": 'caps lock',
        "0x3b": 'f1',
        "0x3c": 'f2',
        "0x3d": 'f3',
        "0x3e": 'f4',
        "0x3f": 'f5',
        "0x40": 'f6',
        "0x41": 'f7',
        "0x42": 'f8',
        "0x43": 'f9',
        "0x44": 'f10',
        "0x47": 'num 7',
        "0x48": 'num 8',
        "0x49": 'num 9',
        "0x4a": 'num -',
        "0x4b": 'num 4',
        "0x4c": 'num 5',
        "0x4d": 'num 6',
        "0x4e": 'num +',
        "0x4f": 'num 1',
        "0x50": 'num 2',
        "0x51": 'num 3',
        "0x52": 'num 0',
        "0x57": 'f11',
        "0x58": 'f12',
        "0x9c": 'keypad enter',
        "0xb5": 'keypad /',
        "0xc7": 'home',
        "0xc8": 'up',
        "0xc9": 'page up',
        "0xcb": 'left',
        "0xcd": 'right',
        "0xcf": 'end',
        "0xd0": 'down',
        "0xd1": 'page down',
        "0xd2": 'insert'
    }

    dcsbios_to_bms_mappings = {
        "ICP_BTN_6 1": "SimICPStpt",
        "ICP_BTN_6 0": "",
    }

    def load_keyfile(self, filepath):
        key_mappings = {}
        with open(filepath, 'r') as file:
            print("Loading key mappings...") # Debugging
            for line in file:
                if not line.startswith("#") and " -1 " not in line:
                    parts = line.split()
                    callback = parts[0]
                    key = parts[3]
                    modifier = parts[4]
                    key_mappings[callback] = (key, modifier)
        print(f"Loaded {len(key_mappings)} key mappings.") # Debugging
        return key_mappings

    def convert_keymap(self, keymap, hex_to_key):
        converted = {}
        for action, (hex_code, state) in keymap.items():
            key_name = hex_to_key.get(hex_code.lower())
            if key_name:
                converted[action] = (key_name, state)
        return converted

    def send_key(self, DCSBIOS_callback):
        if DCSBIOS_callback in self.dcsbios_to_bms_mappings:
            callback = self.dcsbios_to_bms_mappings[DCSBIOS_callback]
            if callback == "":
                return
            key, modifier = self.key_mappings[callback]
            print(f"Sending key: {key} with modifier: {modifier}")
            if modifier == "0":
                keyboard.press_and_release(key)
            elif modifier == "1":
                keyboard.press_and_release('shift+' + key)
            elif modifier == "2":
                keyboard.press_and_release('ctrl+' + key)
            elif modifier == "3":
                keyboard.press_and_release('ctrl+shift+' + key)
            elif modifier == "4":
                keyboard.press_and_release('alt+' + key)
            elif modifier == "5":
                keyboard.press_and_release('shift+alt+' + key)
            elif modifier == "6":
                keyboard.press_and_release('ctrl+alt+' + key)
            elif modifier == "7":
                keyboard.press_and_release('ctrl+shift+alt+' + key)
            time.sleep(0.01)  # Delay to simulate realistic key press timing
        else:
            # If not found in key mappings, check potentiometer mappings
            action_parts = DCSBIOS_callback.split()
            pot_name = action_parts[0]
            # WE SHOULD GET THE VALUE FROM THE DICT HERE:
            axis_code = self.pot_mappings.get(pot_name)

            if pot_name in self.pot_mappings:
                value = int(action_parts[1])
                self.send_pot_value(axis_code, value)
            else:
                print(f"Callback '{DCSBIOS_callback}' not found in key or potentiometer mappings.")

    def send_pot_value(self, axis_code, value):
        value = self.scale_value(value)
        print(value)
        value_hex = hex(value)
        self.joy.set_axis(axis_code, value)
        print(f"Set {axis_code} to {value_hex}")

    def scale_value(self, value):
        # Scale value from 0-65534 to 1-32768
        scaled_value = int((value / 65534) * 32767) + 1
        return scaled_value

    def notify(self, message):
        print("[Falcon-BCC]: {}".format(message))

    def send_message_to_bms(self, line):
        self.notify(f"Sending message to BMS: {line}")
        self.send_key(line)

