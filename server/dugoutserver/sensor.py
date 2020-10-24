
import logging

class DugoutSensor():
    def __init__(self, rs485_client, address, name, description, rs485_addr, toffset=0, hoffset=0):
        self.rs485_client = rs485_client
        self.address = address
        self.name = name
        self.description = description
        self.rs485_addr = rs485_addr
        self.toffset = toffset
        self.hoffset = hoffset

    def get(self):
        logging.debug("Retrieving Data for Sensor {}".format(self.name))
        return {
                "success": True,
                "temperature": 0,
                "humidity": 0
                }

    def apply_offsets(self):
        logging.info("Sensor {}: Applying {}°C and {}% as offset".format(self.name, self.toffset, self.hoffset))
        pass
