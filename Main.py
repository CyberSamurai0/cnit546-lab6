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

    LCD.init_lcd()
    LCD.clear()
    LCD.set_cursor(0,0)

    DHT.init_sensor(0)

    myThermostat = Thermostat()
    Buttons.set_thermostat(myThermostat)

    # Define GPIO pins for stepper motor
    motor = Stepper.StepperMotor(33, 32, 26, 25)

    while True:
        LCD.home()
        LCD.write_string(f"Temp: {0} C")
        
        LCD.set_cursor(1,0)
        LCD.write_string(f"Set:  {myThermostat.temperature} C")

        LCD.set_cursor(3,0)
        LCD.write_string(f"Mode: {myThermostat.modes[myThermostat.mode]} ")

        machine.sleep(100)
        #print((str(toggle_button.value()), str(up_button.value()), str(dn_button.value())))
        continue