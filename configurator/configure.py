#!/usr/bin/python3

from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
import sys
import argparse
import logging

def set_address(target:int, reg_addr=0x0100):
    client = ModbusClient(method = 'rtu', port='/dev/ttyS0',stopbits = 1,timeout =0.3, bytesize = 8, parity = 'N', baudrate = 9600, driver_pin=36)
    connection = client.connect()
    if not connection:
        print("Connection failed. Exiting", file=sys.stderr)
        return 1
    try:
        if target:
            print("Setting address to {}".format(target))
            response = client.write_register(reg_addr,target,unit=0x0000)
            print(response)
    except Exception as e:
        print(e, file=sys.stderr)
    client.close()

#def set_offset(category):
    # not supported here but accessible via a POST request to the server
    # (see dugout-server)
if len(sys.argv)!= 2:
    print("python3 configure.py TARGET_ADDRESS", file=sys.stderr)
    sys.exit(1)
target = int(sys.argv[1])
sys.exit(set_address(target))
