import machine

# For use with Newhaven 20x4 LCD via UART
class LCD:
    def __init__(self, uart_port=1, baudrate=9600, tx_pin=20, rx_pin=21):
        self.lines = ["", "", "", ""]
        
        # Initialize UART for LCD communication
        self.uart = machine.UART(uart_port, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
        self.uart.init(bits=8, parity=None, stop=1)

        # Turn on LCD Backlight
        self.uart.write(bytearray([0x41]))
        self.clear()
        self.home()

    def send_command(self, cmd):
        self.uart.write(bytearray([0xFE, cmd]))

    def set_cursor_addr(self, addr):
        self.uart.write(bytearray([0xFE, 0x45, addr]))

    def set_cursor(self, row, col):
        # Handle out-of-bounds values
        row = 0 if row < 0 else row
        row = 3 if row > 3 else row
        col = 0 if col < 0 else col
        col = 19 if col > 19 else col

        # Store calculated position value
        pos = 0

        if row == 0:
            pos = 0
        elif row == 1:
            pos = 0x40
        elif row == 2:
            pos = 0x14
        elif row == 3:
            pos = 0x54
        
        pos += col

        # Send command to set cursor position
        self.set_cursor_addr(pos)

    def clear(self):
        self.send_command(0x51) # Clear display command

    def home(self):
        self.send_command(0x46) # Return home command

    def write_string(self, s):
        self.uart.write(s.encode('utf-8')) # Send string to LCD

    def set_line(self, line_num, text):
        if line_num < 0 or line_num > 3:
            return
        
        # Pad text with spaces and truncate to 20 chars
        self.lines[line_num] = f"{text:<20}"[:20]
        self.set_cursor(line_num, 0)
        self.write_string(self.lines[line_num])