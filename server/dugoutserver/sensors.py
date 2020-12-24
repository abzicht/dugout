try:
    from sensor import DugoutSensor
except ImportError:
    from dugoutserver.sensor import DugoutSensor

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import serial
import logging

class DugoutSensors():
    def __init__(self, config):
        self.sensors = []
        self.client = None #todo
        self.init_client()
        self.init_sensors(config)

    def init_client(self):
        self.client= ModbusClient(method = 'rtu', port='/dev/ttyS0', stopbits = 1,timeout =0.3, bytesize = 8, parity = 'N', baudrate = 9600, driver_pin=36)
        connection = self.client.connect()
        if not connection:
            raise serial.SerialException("Unable to connect to serial!")

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
    
    def set(self, calibration_config):
        """
        provide a dict of that format:
        {
        "Sensor 1": { # Sensor name (found in config)
            "temperature": -1.5, # Temperature offset (optional)
            "humidity": 5, # Humidity offset (optional)
            },
        ...
        }
        """
        success = True
        logging.info("Performing Sensor Calibration")
        for sensor in self.sensors:
            if sensor.name in calibration_config.keys():
                sensor_config = calibration_config[sensor.name]
                temperature = None
                humidity = None
                if 'temperature' in sensor_config:
                    temperature = sensor_config['temperature']
                if 'humidity' in sensor_config:
                    humidity = sensor_config['humidity']
                logging.info("Setting offsets for {} - T: {}, H: {}".format(sensor.name,temperature, humidity))
                success = False if not sensor.set(temperature = temperature, humidity = humidity) else success
        return success 

    def stop(self):
        logging.debug("Stopping Dugout Sensors")
        self.client.close()
