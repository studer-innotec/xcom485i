# Read parameter 1107, Maximum current of AC source, (Modbus register 14) from the first Xtender
# Run this example within the 'examples/' folder using 'python ex_read_param.py' from a CLI after installing
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

        # read actual value stored into flash memory
        read_value = xcom485i.read_parameter(xcom485i.addresses.xt_1_device_id,
                                             14 + xcom485i.addresses.read_param_flash_offset)
        print('read_value:', read_value)

        # read minimum value of this parameter
        read_value = xcom485i.read_parameter(xcom485i.addresses.xt_1_device_id,
                                             14 + xcom485i.addresses.read_param_min_offset)
        assert read_value == 2.0  # only for 1107 parameter
        print('read_min_value:', read_value)

        # read maximum value of this parameter
        read_value = xcom485i.read_parameter(xcom485i.addresses.xt_1_device_id,
                                             14 + xcom485i.addresses.read_param_max_offset)
        assert read_value == 50.0  # only for 1107 parameter
        print('read_max_value:', read_value)
