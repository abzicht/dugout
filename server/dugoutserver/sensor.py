from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

import logging

class DugoutSensor():
    max_attempts = 100 # the number of attempts to contact the sensor

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

    def set(self, temperature:float = None, humidity:float = None):
        success_t = True
        success_h = True
        if temperature:
            temp = int(temperature * 10)
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_int(temp)
            payload = builder.to_registers()[0]
            print(payload)
            #payload = builder.build()
            #print(payload)
            for i in range(0, DugoutSensor.max_attempts):
                logging.debug("Setting temperature offset for Sensor {} at attempt {}".format(self.name, i+1))
#                try:
                    #self.rs485_client.write_register(0x0103, payload, unit=self.rs485_addr)
                response = self.rs485_client.write_register(0x0003, 0x005, unit=self.rs485_addr)
                print(response)
#                except Exception as e:
#                    #logging.debug(e)
#                    print(e)
#                    success_t = False
#                else:
#                    success_t = True
                self.toffset = temperature
#                    break
        if humidity:
            pass
        return success_t
