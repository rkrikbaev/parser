#!.venv/bin/python
# -*- coding: utf-8 -*-
# read_register# read 10 registers and print result on stdout
# you can use the tiny modbus server "mbserverd" to test this code# mbserverd is here: https://github.com/sourceperl/mbserverd
# the command line modbus client mbtget can also be useful
# mbtget is here: https://github.com/sourceperl/mbtget

from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.1.248"
SERVER_PORT = 5020
c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, unit_id=1)

# uncomment this line to see debug message
# c.debug(True)
# define modbus server host, port

# c.host(SERVER_HOST)   
# c.port(SERVER_PORT)

while True:
    # open or reconnect TCP to server if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
        # if open() is ok, read register (modbus function 0x03)
    if c.is_open:
        # read 10 registers at address 0, store result in regs list
        regs = c.read_holding_registers(100, 10)
        # if success display registers
        if regs:
            print("reg ad #0 to 4: "+str(regs))
            # sleep 2s before next polling
            time.sleep(2)
    else:
        time.sleep(10)