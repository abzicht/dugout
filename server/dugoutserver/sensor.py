from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

import logging

class DugoutSensor():
    max_attempts = 5 # the number of attempts to contact the sensor

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
        temperature = 0
        humidity    = 0
        success_t   = True
        success_h   = True
        for i in range(0, DugoutSensor.max_attempts):
            logging.debug("Retrieving temperature data for Sensor {} at attempt {}".format(self.name, i+1))
            try:
                temperature_read = self.rs485_client.read_input_registers(0x0000, count=1, unit=self.rs485_addr)
                decoder_t = BinaryPayloadDecoder.fromRegisters(temperature_read.registers, byteorder=Endian.Big)
                temperature = decoder_t.decode_16bit_int() / 10
            except Exception as e:
                logging.debug(e)
                success_t = False
            else:
                success_t = True
                break
        for i in range(0, DugoutSensor.max_attempts):
            logging.debug("Retrieving Humidity data for Sensor {} at attempt {}".format(self.name, i+1))
            try:
                humidity_read = self.rs485_client.read_input_registers(0x0001, count=1, unit=self.rs485_addr)
                decoder_h = BinaryPayloadDecoder.fromRegisters(humidity_read.registers, byteorder=Endian.Big)
                humidity = decoder_h.decode_16bit_uint() / 10
            except Exception as e:
                logging.debug(e)
                success_h = False
            else:
                success_h = True
                break
        return {
                "success_t": success_t,
                "success_h": success_h,
                "temperature": temperature,
                "humidity": humidity
                }

    def apply_offsets(self):
        logging.warn("This functionality is not implemented")
        logging.info("Sensor {}: Applying {}°C and {}% as offset".format(self.name, self.toffset, self.hoffset))
        pass
