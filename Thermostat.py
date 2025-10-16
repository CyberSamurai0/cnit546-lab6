class Thermostat:
    # Define Mode Strings
    modes = ["OFF", "HEAT", "COOL"]

    def __init__(self, temperature=22, mode=0, screen=None):
        self.temperature = temperature
        self.mode = mode
        self.screen = screen

    def set_temperature(self, temperature):
        self.temperature = temperature
        if self.screen:
            self.screen.set_line(1, f"Set:  {self.temperature} C")
        print(f"Temperature set: {self.temperature}")

    def temp_up(self):
        self.temperature += 1
        if self.screen:
            self.screen.set_line(1, f"Set:  {self.temperature} C")
        print(f"Temperature up: {self.temperature}")

    def temp_down(self):
        self.temperature -= 1
        if self.screen:
            self.screen.set_line(1, f"Set:  {self.temperature} C")
        print(f"Temperature down: {self.temperature}")

    def set_mode(self, mode):
        self.mode = mode % 3
        if self.screen:
            self.screen.set_cursor(0, 16) # Write to end of line
            self.screen.write_string((self.modes[self.mode] + "    ")[:4]) # Ensure always 4 chars
            #self.screen.set_line(3, f"Mode: {self.modes[self.mode]} ")
        print(f"Mode set: {self.modes[self.mode]}")