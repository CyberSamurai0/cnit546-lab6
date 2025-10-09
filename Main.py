# Import Built-In Libraries
import machine

# Import Custom Libraries
import Stepper
import Buttons
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


    myThermostat = Thermostat()
    Buttons.set_thermostat(myThermostat)

    # Define GPIO pins for stepper motor
    motor = Stepper.StepperMotor(33, 32, 26, 25)

    while True:
        #print((str(toggle_button.value()), str(up_button.value()), str(dn_button.value())))
        continue