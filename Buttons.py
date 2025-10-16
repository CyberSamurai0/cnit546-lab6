import machine

# Module-level reference to the Thermostat instance
_thermostat = None

# Setter to allow Main.py to provide the Thermostat instance
def set_thermostat(instance):
    global _thermostat
    _thermostat = instance


# Initialize Buttons with Interrupts
def init_mode_toggle_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=mode_toggle_handler)

def init_temp_up_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=temp_up_handler)

def init_temp_dn_button(pin):
    pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=temp_dn_handler)


# Create Handler Functions for Interrupts
def mode_toggle_handler(_):
    if _thermostat is not None:
        _thermostat.set_mode(_thermostat.mode + 1)
    else:
        print("Thermostat instance not set!")

def temp_up_handler(_):
    if _thermostat is not None:
        _thermostat.temp_up()
    else:
        print("Thermostat instance not set!")

def temp_dn_handler(_):
    if _thermostat is not None:
        _thermostat.temp_down()
    else:
        print("Thermostat instance not set!")