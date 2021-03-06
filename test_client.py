import os
import yaml
ROOT = os.path.abspath(os.path.dirname(__file__))
from paho.mqtt.client import Client as MQTTClient
import numpy as np
import time
from test_server import test_settings, server


def run_client(settings):
    def on_connect(*args, **kwargs):
        print("connected")

    def on_message(*args, **kwargs):
        print("message received", args, kwargs)

    client = MQTTClient()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(server, settings["mqtt_settings"]["port"], 60)
    t0 = time.time()
    while True:
        time.sleep(1)
        client.loop()
        td = time.time()-t0
        f = lambda x: np.log(x/10)*10+50
        data = '{"meat_temp": %.1f, "oven_temp": %.1f}' % (f(td), f(td+100))
        print("publishing data")
        client.publish("test_topic", data)


if __name__ == "__main__":
    settings = yaml.load(test_settings)
    run_client(settings)
