try:
    from sensor import DugoutSensor
except ImportError:
    from dugout.sensor import DugoutSensor

import logging

class DugoutSensors():
    def __init__(self, config):
        self.sensors = []
        self.client = None #todo
        self.init_sensors(config)

    def init_sensors(self, config):
        for address in config.keys():
            sensor = DugoutSensor(self.client, address,
                    config[address]["name"],
                    config[address]["description"],
                    config[address]["rs485_addr"],
                    config[address]["toffset"],
                    config[address]["hoffset"])
            self.sensors += [sensor]
    def get(self):
        response = {}
        logging.info("Retrieving Sensor Data")
        for sensor in self.sensors:
            response[sensor.address] = sensor.get()
        logging.debug("Retrieved Sensor Data")
        return response

    def stop(self):
        logging.debug("Stopping Dugout Sensors")

sensors = {
    1: {
        "success": True,
        "temperature": -0.5,
        "humidity": 52,
        },
    2: {
        "success": True,
        "temperature": 20.5,
        "humidity": 62,
        }
}
