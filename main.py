import os
import time

import dirigera
from prometheus_client import Gauge
from prometheus_client import start_http_server

DIRIGERA_HOST = os.getenv("DIRIGERA_HOST")
DIRIGERA_TOKEN = os.getenv("DIRIGERA_TOKEN")

EXPORTER_PORT = os.getenv("EXPORTER_PORT")
EXPORTER_REFRESH_INTERVAL = os.getenv("EXPORTER_REFRESH_INTERVAL")


dirigera_hub = dirigera.Hub(
    token=DIRIGERA_TOKEN,
    ip_address=DIRIGERA_HOST,
)

g = Gauge('dirigera_device_battery_percentage', 'Battery percentage of a specific device', ['id', 'type', 'room_id', 'room_namme'])

g2 = Gauge('dirigera_openclose_sensor_isopen', 'sensor state', ['id', 'type', 'room_id', 'room_namme'])


port = int(EXPORTER_PORT) if EXPORTER_PORT else 8312
refresh_interval = int(EXPORTER_REFRESH_INTERVAL) if EXPORTER_REFRESH_INTERVAL else 15

start_http_server(port)

while True:

    print("Updating...")
    for s in dirigera_hub.get_open_close_sensors():
        g.labels(s.id, s.type, s.room.id, s.room.name).set(s.attributes.battery_percentage)
        g2.labels(s.id, s.type, s.room.id, s.room.name).set(s.attributes.is_open)


    time.sleep(refresh_interval)