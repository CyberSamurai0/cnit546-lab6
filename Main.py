# Import Built-In Libraries
import machine
import ujson
import time

# Import Custom Libraries
import Stepper
import Buttons
import LCD
import DHT
import Network
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
            screen.set_cursor(0, 0)
            screen.write_string(f"Temp: {temperature} C")
        else:
            screen.set_cursor(0, 0)
            screen.write_string("Temp: -- C")

    sensor = DHT.Sensor(0)
    sensor.start_periodic_read(2000, sensorOnRead)

    myThermostat = Thermostat(22, 0, screen)
    Buttons.set_thermostat(myThermostat)

    # Initial Display
    screen.set_cursor(0, 0)
    screen.write_string(f"Temp: -- C")
    screen.set_cursor(0, 16) # Write to end of line
    screen.write_string(f"{myThermostat.modes[myThermostat.mode]}")
    screen.set_line(1, f"Set:  {myThermostat.temperature} C")
    #screen.set_line(3, f"Mode: {myThermostat.modes[myThermostat.mode]} ")
    screen.set_line(3, f"Out:  -- C")

    # Define GPIO pins for stepper motor
    motor = Stepper.StepperMotor(33, 32, 26, 25)

    def rpc_callback(topic, msg):
        print("Received message:", msg)
        try:
            data = ujson.loads(msg)
            if data["method"] == "setOutside":
                outside = data["params"]
                if isinstance(outside, (int, float)):
                    screen.set_line(3, f"Out:  {int(outside)} C")
            elif data["method"] == "setPower":  
                power = data["params"]
                if (power == False):
                    myThermostat.set_mode(0) # Set to OFF
                else:
                    myThermostat.set_mode(1) # Set to HEAT
            elif data["method"] == "setMode":
                mode = data["params"]
                if mode in [0, 1, 2]:
                    myThermostat.set_mode(mode)
            elif data["method"] == "setTemp":
                temp = data["params"]
                if isinstance(temp, int) and (16 <= temp <= 30):
                    myThermostat.set_temperature(temp)
            elif data["method"] == "setFan":
                fanOn = data["params"]
                if fanOn:
                    motor.start_rotation(5) # Rotate indefinitely
                else:
                    motor.stop_rotation()
        except Exception as e:
            print("Error processing message:", e)

    # Connect to Wi-Fi
    wlan = Network.connect_to_wifi("Phone Hotspot", "password")
    try:
        mqtt_client = Network.init_MQTT("mqtt.thingsboard.cloud", "token", "", rpc_callback, 1883)
    except Exception as e:
        print("MQTT connect failed:", e)

    while True:
        telemetry = {
            "temperature": sensor.temperature,
            "humidity": sensor.humidity,
            "setpoint": myThermostat.temperature,
            "mode": myThermostat.mode
        }
        Network.publish_message(mqtt_client, "v1/devices/me/telemetry", ujson.dumps(telemetry))
        time.sleep(10)