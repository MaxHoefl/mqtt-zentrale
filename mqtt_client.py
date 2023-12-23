import os
from pathlib import Path
import paho.mqtt.client as mqtt
from loguru import logger


TOPIC = "house/main"


def configure_logger():
    root_dir = Path(__file__).parent.joinpath("mqtt-client.logs")
    logger.add(root_dir, level="INFO")


def configure_mqtt_client():
    broker_address = os.environ.get("MQTT_BROKER_ADDRESS", "raspberrypi.local")
    client_name = os.environ.get("MQTT_CLIENT_NAME", "master")
    client = mqtt.Client(client_name)

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    logger.info("Connecting to broker")
    client.connect(broker_address)
    return client


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with result code {rc}")
    client.subscribe(TOPIC)


def on_subscribe(*args, **kwargs):
    logger.info(f"Subscribed to topic '{TOPIC}'")


def on_message(client, userdata, message):
    logger.info(f"Got message: {message.payload.decode('utf-8')}")
    pass


def on_disconnect(*args, **kwargs):
    logger.warning("Client disconnected")


def main():
    configure_logger()
    client = configure_mqtt_client()

    try:
        client.loop_forever()
    finally:
        logger.info("Shutting down")
        client.loop_stop()
        client.disconnect()


if __name__ == '__main__':
    main()
