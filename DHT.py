import machine
import dht

class Sensor:
    def __init__(self, pin):
        self.sensor = dht.DHT11(machine.Pin(pin, machine.Pin.IN))
        self.temperature = -1
        self.humidity = -1
        self._timer = None
        self._callback = None

    def start_periodic_read(self, interval_ms=2000, callback=None):
        self._callback = callback
        if self._timer is None:
            self._timer = machine.Timer(0)
            self._timer.init(period=interval_ms, mode=machine.Timer.PERIODIC, callback=self._read)

    def stop_periodic_read(self):
        if self._timer:
            self._timer.deinit()
            self._timer = None
    
    def _read(self, _):
        try:
            self.sensor.measure()
            self.temperature = self.sensor.temperature()
            self.humidity = self.sensor.humidity()
            if self._callback:
                self._callback(self.temperature, self.humidity)
        except Exception as e:
            print("Error reading sensor:", e)
            self.temperature = -1
            self.humidity = -1