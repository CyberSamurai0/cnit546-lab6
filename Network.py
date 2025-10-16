import network
import machine
from umqtt.simple import MQTTClient

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to Wi-Fi:', wlan.ifconfig())
    return wlan

def init_MQTT(server, user, password, callback, port=1883):
    client = MQTTClient(
        client_id="esp32",
        server=server,
        user=user,
        password=password,
        port=port
    )
    client.set_callback(callback)
    print("Constructed MQTT client")
    client.connect()
    print('Connected to MQTT broker')
    client.subscribe(b"v1/devices/me/rpc/request/+")
    print("Subscribed to RPC topic")

    def _read(t):
        client.check_msg()


    MQTT_Timer = machine.Timer(1)
    MQTT_Timer.init(period=50, mode=machine.Timer.PERIODIC, callback=_read)

    return (client, MQTT_Timer)


def publish_message(client, topic, message):
    client.publish(topic, message)
    print("Published updated cloud telemetry")