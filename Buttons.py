import machine

# Module-level reference to the Thermostat instance
_thermostat = None

# Setter to allow Main.py to provide the Thermostat instance
def set_thermostat(instance):
    global _thermostat
    _thermostat = instance


# Initialize Buttons with Interrupts
def init_mode_toggle_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=mode_toggle_handler)

def init_temp_up_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=temp_up_handler)

def init_temp_dn_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=temp_dn_handler)


# Create Handler Functions for Interrupts
def mode_toggle_handler(_):
    if _thermostat is not None:
        _thermostat.mode = (_thermostat.mode + 1) % 3
        print(f"Mode changed to {_thermostat.modes[_thermostat.mode]}")
    else:
        print("Thermostat instance not set!")

def temp_up_handler(_):
    if _thermostat is not None:
        _thermostat.temp_up()
        print(f"Mode changed to {_thermostat.modes[_thermostat.mode]}")
    else:
        print("Thermostat instance not set!")

def temp_dn_handler(_):
    if _thermostat is not None:
        _thermostat.temp_down()
        print(f"Mode changed to {_thermostat.modes[_thermostat.mode]}")
    else:
        print("Thermostat instance not set!")