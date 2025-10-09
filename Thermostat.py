class Thermostat:
    # Define Mode Strings
    modes = ["OFF", "HEAT", "COOL"]

    def __init__(self, temperature=72, mode=0):
        self.temperature = temperature
        self.mode = mode

    def temp_up(self):
        self.temperature += 1
        print(f"Temperature up: {self.temperature}")

    def temp_down(self):
        self.temperature -= 1
        print(f"Temperature down: {self.temperature}")