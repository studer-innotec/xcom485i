# Write parameter 1107 in RAM only, Maximum current of AC source, (Modbus register 14) from the first Xtender
# Run this example within the 'examples/' folder using 'python ex_write_param.py' from a CLI after installing
#   xcom485i package with 'pip install xcom485i'

import serial
from xcom485i.client import Xcom485i

SERIAL_PORT_NAME = 'COM4'  # your serial port interface name
SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

if __name__ == "__main__":
    try:
        serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE, parity=serial.PARITY_EVEN, timeout=1)
    except serial.serialutil.SerialException as e:
        print("Check your serial configuration : ", e)
    else:
        xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=True)

        value = 8  # 8 [A]
        echo = xcom485i.write_parameter(xcom485i.addresses.xt_1_device_id, 14 + xcom485i.addresses.write_param_ram_only,
                                        value)
        assert echo == 2  # a value of 2 is expected on write action, represent the number of registers written
        print('echo:', echo)
