# Read all pending messages stored into the gateway
# Run this example within the 'examples/' folder using 'python ex_read_messages.py' from a CLI after installing
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
        pending_message_count = xcom485i.pending_message_count()  # always check the number of pending messages
        print('pending_message_count:', pending_message_count)

        for _ in range(pending_message_count):
            message_registers = xcom485i.message_registers()
            print('Message N°:', _)
            print("\t device source: ", message_registers[0])
            print("\t message id: ", message_registers[1])
            print("\t optionnal most significant word: ", message_registers[2])
            print("\t optionnal least significant word: ", message_registers[3])
