import machine

# For use with Newhaven 20x4 LCD via UART

def init_lcd():
    # Initialize UART1 for LCD communication
    global uart1
    uart1 = machine.UART(1, baudrate=9600, tx=20, rx=21)
    uart1.init(bits=8, parity=None, stop=1)
    
    # Turn on LCD Backlight
    uart1.write(bytearray([0x41]))


# Send a command byte to the LCD
def send_command(cmd):
    uart1.write(bytearray([0xFE, cmd]))

def set_cursor_addr(addr):
    uart1.write(bytearray([0xFE, 0x45, addr]))

# Set cursor position (row: 0-3, col: 0-19)
def set_cursor(row, col):
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
    set_cursor_addr(pos)

def clear():
    send_command(0x51)  # Clear display command

def home():
    send_command(0x46)  # Return home command

def write_string(s):
    uart1.write(s.encode('utf-8'))  # Send string to LCD