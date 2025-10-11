# Import Built-In Libraries
import machine

# Import Custom Libraries
import Stepper
import Buttons
import LCD
import DHT
from Thermostat import Thermostat

# Heat/Cool Toggle
toggle_button = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

# Temperature Up/Down Buttons
up_button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
dn_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

if __name__ == "__main__":
    print("Running!")

    Buttons.init_mode_toggle_button(toggle_button)
    Buttons.init_temp_up_button(up_button)
    Buttons.init_temp_dn_button(dn_button)

    screen = LCD.LCD()

    # Define callback for DHT periodic readings
    def sensorOnRead(temperature, _):
        if temperature != -1:
            screen.set_line(0, f"Temp: {temperature} C")
        else:
            screen.set_line(0, "Temp: -- C")

    sensor = DHT.Sensor(0)
    sensor.start_periodic_read(2000, sensorOnRead)

    myThermostat = Thermostat(22, 0, screen)
    Buttons.set_thermostat(myThermostat)

    # Initial Display
    screen.set_line(0, f"Temp: -- C")
    screen.set_line(1, f"Set:  {myThermostat.temperature} C")
    screen.set_line(3, f"Mode: {myThermostat.modes[myThermostat.mode]} ")

    # Define GPIO pins for stepper motor
    motor = Stepper.StepperMotor(33, 32, 26, 25)

    while True:
        continue