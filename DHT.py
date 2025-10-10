import machine
import dht

def init_sensor(pin):
    return dht.DHT11(machine.Pin(pin, machine.Pin.IN))

def read_sensor(sensor):
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        return temp, hum
    except Exception as e:
        print("Error reading sensor:", e)
        return None, None