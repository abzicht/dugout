#!/usr/bin/python3

from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client= ModbusClient(method = 'rtu', port='/dev/ttyS0',stopbits = 1,timeout =0.3, bytesize = 8, parity = 'N', baudrate = 9600, driver_pin=36)

connection = client.connect()

print("Connection", connection)

def read_device(address, attempts=1):
    try:
        for i in range(0,attempts):
            if connection:
                try:
                    temperature = client.read_input_registers(0x0000, count=1, unit=address)
                    decoder_t = BinaryPayloadDecoder.fromRegisters(temperature.registers, byteorder=Endian.Big)
                    temperature_ = decoder_t.decode_16bit_int() / 10
                    humidity = client.read_input_registers(0x0001, count=1, unit=address)
                    decoder_h = BinaryPayloadDecoder.fromRegisters(humidity.registers, byteorder=Endian.Big)
                    humidity_ = decoder_h.decode_16bit_uint() / 10
                    print(temperature_, "°C", humidity_, "%")
                except Exception as e:
                    print(e)
    except KeyboardInterrupt:
        client.close()

def get_set_address(source=0x01, reg_addr=0x0100, target=None):
    try:
        address = client.read_holding_registers(reg_addr,1,unit=source)
        decoder_a = BinaryPayloadDecoder.fromRegisters(address.registers, byteorder=Endian.Big)
        address_ = decoder_a.decode_16bit_uint()
        print("Source: {} (register address: {})".format(address_, reg_addr))
        if target:
            print("Setting address from {} to {}.".format(source, target))
            response = client.write_register(reg_addr,target,unit=0x0000)
        address = client.read_holding_registers(reg_addr,1,unit=target)
        decoder_a = BinaryPayloadDecoder.fromRegisters(address.registers, byteorder=Endian.Big)
        address_ = decoder_a.decode_16bit_uint()
        print("New Source:", address_)

    except Exception as e:
        print(e)

#read_device(8,5)
read_device(1,5)
#try:
#    for i in range(0,0x0200):
#        get_set_address(1,i)
#except KeyboardInterrupt:
#    client.close()
#get_set_address(0x0001,reg_addr=0x0000,target=0x0008)

client.close()
