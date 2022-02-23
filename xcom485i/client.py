#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Warnings
--------
Changing parameters when the inverters are in operation should be done carefully. The
modification of parameters can restart the corresponding algorithm inside the inverter. For
example, the change of a delay can restart the timer attached to it.

When you are using the *RCC* remote control, the *Xtender* inverter/charger, *VarioTrack* and
*VarioString MPPT* solar chargers store their parameter values in a non-volatile flash memory.
Because of the endurance of this memory, the number of writes on a single parameter is only
**guaranteed for 1000 write operations**.
To allow the cyclic write of parameters without count limit, we suggest you to write the
parameters in RAM only
"""

from struct import pack, unpack
from datetime import datetime
from umodbus.client.serial import rtu
from umodbus.exceptions import *
from xcom485i.addresses import Addresses
import logging

logger = logging.getLogger(__name__)


class Xcom485i:
    """
    This class act as a *Modbus* master in order to communicate with the *Xcom-485i* gateway (slave)

    Attributes
    ----------
    serial_port: serial.Serial
        Serial port used for communication with the gateway
    addresses: xcom485i.addresses.Addresses
        Instance of Addresses class grouping all the ones accessible from the Xcom-485i
    """

    def __init__(self, serial_port, offset=0, debug=False):
        """
        serial device must be configured with :\n
        - EVEN parity\n
        - 1 start bit\n
        - 8 data bits, LSB first\n
        - 1 parity bit (Even)\n
        - 1 stop bit\n
        - timeout 1 second\n
        Parameters
        ----------
        serial_port
            Instance of serial module
        offset
            The address offset as defined with the dip-switches
        debug: boolean
            Activate debug traces for tx/rx frames
        """
        self.serial_port = serial_port
        if debug is True:
            logging.basicConfig(level=logging.DEBUG)
        self.addresses = Addresses(offset)

    def __del__(self):
        """
        Explicit destructor
        Ensure to close serial device
        Returns
        -------
        None
        """
        self.serial_port.close()

    def read_parameter(self, slave_id, address):
        """
        Read a parameter from a targeted device as a float.

        Note
        -----
        All parameters accessible from *RCC* can also be accessed with the *Modbus* protocol.\n
        It is possible to read the actual value of the parameter from Flash, but also the
        minimum and the maximum value.\n
        To distinguish between these, we use a different register address offset as explained below:\n
        - read value from flash   : offset is 0    (READ_PARAM_FLASH_OFFSET)\n
        - read min allowed value  : offset is 2000 (READ_PARAM_MIN_OFFSET)\n
        - read max allowed value  : offset is 4000 (READ_PARAM_MAX_OFFSET)\n

        Parameters
        ----------
        slave_id: int
            Slave identifier number (targeted device)
        address: int
            Register starting address, see Studer Modbus RTU Appendix for the complete list of accessible register per
            device

        Returns
        -------
        float
            parameter read

        Example
        --------
        .. code-block:: python

            # Read parameter 1107, Maximum current of AC source, (Modbus register 14) from the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_read_param.py' from a CLI
            #   after installing xcom485i package with 'pip install xcom485i'

            import serial
            from xcom485i.client import Xcom485i

            SERIAL_PORT_NAME = 'COM4'  # your serial port interface name
            SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
            DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

            if __name__ == "__main__":
                try:
                    serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE,
                                                parity=serial.PARITY_EVEN, timeout=1)
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
        """
        message = rtu.read_holding_registers(slave_id=slave_id, starting_address=address, quantity=2)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            ba = pack('>HH', response[0], response[1])
            float_response = unpack('>f', ba)[0]
            logger.debug("<- Receive data : 0x%s", str(ba.hex()))
            return float_response

    def read_time(self, slave_id):
        """
        Read the system time from a targeted installation.

        Note
        -----
        The system time is available at the address 0 of the device system.\n
        The time registers are accessible separetely if needed by using the correct address and length.\n
        Here is the list of time registers:\n
        - 0 -> Microsecond\n
        - 1 -> Second\n
        - 2 -> Minute\n
        - 3 -> Hour\n
        - 4 -> Weekday\n
        - 5 -> Day\n
        - 6 -> Month\n
        - 7 -> Year (format 2022 = 22)\n

        Parameters
        ----------
        slave_id: int
            Slave identifier number (targeted device)

        Returns
        -------
        datetime
            actual system time

        Example
        --------
        .. code-block:: python

            # Read the system time
            # Run this example within the 'examples/' folder using 'python ex_read_time.py' from a CLI after installing
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
                    read_value = xcom485i.read_time(xcom485i.addresses.system_device_id)
                    print('Read time:', read_value)
        """
        message = rtu.read_holding_registers(slave_id=slave_id, starting_address=0, quantity=8)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            return datetime(response[7], response[6], response[5], response[3], response[2], response[1], response[0]*1000)
            
    def write_parameter(self, slave_id, address, value):
        """
         Write a parameter value into a targeted device.

        Note
        -----
        All parameters accessible from *RCC* can also be accessed with the *Modbus* protocol.\n
        In the *Xtender* system, it is possible to write a value in Flash (and RAM) or in RAM
        only.\n
        To distinguish between both, we use a different register address offset as explained below:\n
        - write value into FLASH and RAM  : offset is 0    (WRITE_PARAM_FLASH_RAM)\n
        - write value into RAM only       : offset is 6000 (WRITE_PARAM_RAM_ONLY)\n

        Parameters
        ----------
        slave_id
            Slave identifier number (targeted device)
        address
            Register starting address, see *Studer Modbus RTU Appendix* for the complete list of accessible
            register per device
        value
            The value to write

        Returns
        -------
        int
            Quantity of written registers (must be 2)

        Example
        --------
        .. code-block:: python

            # Write parameter 1107 in RAM only, Maximum current of AC source, (Modbus register 14)
            #   from the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_write_param.py' from a CLI
            #   after installing xcom485i package with 'pip install xcom485i'

            import serial
            from xcom485i.client import Xcom485i

            SERIAL_PORT_NAME = 'COM4'  # your serial port interface name
            SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
            DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

            if __name__ == "__main__":
                try:
                    serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE,
                                                parity=serial.PARITY_EVEN, timeout=1)
                except serial.serialutil.SerialException as e:
                    print("Check your serial configuration : ", e)
                else:
                    xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=True)

                    value = 8  # 8 [A]
                    echo = xcom485i.write_parameter(xcom485i.addresses.xt_1_device_id,
                                                    14 + xcom485i.addresses.write_param_ram_only, value)
                    # a value of 2 is expected on write action, represent the number of registers written
                    assert echo == 2
                    print('echo:', echo)
        """
        ba = pack('>f', value)
        registers = unpack('>HH', ba)
        message = rtu.write_multiple_registers(slave_id=slave_id, starting_address=address, values=registers)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            logger.debug("<- Receive data : 0x%s", str(response))
            return response

    def write_time(self, slave_id, value):
        """
        Write the time of a targeted installation.

        Note
        -----
        It is only possible to set the time and date by writting all registers at the same time.\n
        Here is the list of time registers:\n
        - 0 -> Microsecond\n
        - 1 -> Second\n
        - 2 -> Minute\n
        - 3 -> Hour\n
        - 4 -> Weekday\n
        - 5 -> Day\n
        - 6 -> Month\n
        - 7 -> Year (format 2022 = 22)\n

        Parameters
        ----------
        slave_id
            Slave identifier number (targeted device)
        value
            The new datetime to write

        Returns
        -------
        int
            Quantity of written registers (must be 8)

        Example
        --------
        .. code-block:: python

            # Write the system time
            # Run this example within the 'examples/' folder using 'python ex_write_time.py' from a CLI after installing
            #   xcom485i package with 'pip install xcom485i'

            import serial
            from xcom485i.client import Xcom485i
            from datetime import datetime

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

                    # current date and time
                    current_dt = datetime.now()
                    print(current_dt)
                    echo = xcom485i.write_time(xcom485i.addresses.system_device_id, current_dt)
                    assert echo == 8  # a value of 2 is expected on write action, represent the number of registers written
                    print('echo:', echo)
        """
        registers = [int(value.microsecond / 1000),
                        value.second,
                        value.minute,
                        value.hour,
                        value.weekday(),
                        value.day,
                        value.month,
                        value.year]
        message = rtu.write_multiple_registers(slave_id=slave_id, starting_address=0, values=registers)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            logger.debug("<- Receive data : 0x%s", str(response))
            return response

    def read_info(self, slave_id, address):
        """
        Read a user info from a targeted device as a float.

        Note
        -----
        The available user information is the same as the values that can be chosen to be displayed
        on the *RCC*. This user information gives the current state of the system. The user information can
        not be modified and their values change during the operation of the system.

        Parameters
        ----------
        slave_id
            Slave identifier number (targeted device)
        address
            Register starting address, see *Studer Modbus RTU Appendix* for the complete list of accessible
            register per device

        Returns
        -------
        float
            User info read

        Example
        --------
        .. code-block:: python

            # Read user info 3001, Battery temperature, (Modbus register 2) from the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_read_info.py' from a CLI
            #   after installing xcom485i package with 'pip install xcom485i'

            import serial
            from xcom485i.client import Xcom485i

            SERIAL_PORT_NAME = 'COM4'  # your serial port interface name
            SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
            DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

            if __name__ == "__main__":
                try:
                    serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE,
                                                parity=serial.PARITY_EVEN, timeout=1)
                except serial.serialutil.SerialException as e:
                    print("Check your serial configuration : ", e)
                else:
                    xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=True)
                    read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, 2)
                    print('read_value:', read_value)
        """
        message = rtu.read_input_registers(slave_id=slave_id, starting_address=address, quantity=2)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            ba = pack('>HH', response[0], response[1])
            float_response = unpack('>f', ba)[0]
            logger.debug("<- Receive data : 0x%s", str(ba.hex()))
            return float_response

    def read_input_registers(self, slave_id, address, quantity):
        """
        Get raw data from input registers.

        Parameters
        ----------
        slave_id
            Slave identifier number (targeted device)
        address
            Register starting address
        quantity
            Quantity of registers to read

        Returns
        -------
        bytes
            Raw data from targeted registers
        """
        message = rtu.read_input_registers(slave_id=slave_id, starting_address=address, quantity=quantity)
        logger.debug("-> Transmit ADU : 0x%s", str(bytes(message).hex()))
        try:
            response = rtu.send_message(message, self.serial_port)
        except (ValueError, KeyError) as e:
            logger.error(
                "--> Please match your configurations and the values set with the dip-switches on the device: ", e)
        except ModbusError as e:
            logger.error("--> Modbus error : ", e)
        else:
            hex_response = ' '.join(hex(x) for x in response)
            logger.debug("<- Receive data : %s", str(hex_response))
            return response

    def pending_message_count(self):
        """
        Get the number of currently pending messages stored into the gateway, by reading the content of
        the 0x0000 input register.

        Note
        -----
        Within the *Xtender* system, any device (*Xtender*, *VarioTrack*, *VarioString*, *BSP*, *Xcom-CAN BMS*)
        can send messages. These messages are displayed on the *RCC* and also available on the
        *Studer Portal* whenever the installation is connected to the Internet.

        Returns
        -------
        int
            The number of pending messages (up to 128)

        See also
        --------
        Xcom485i.message_registers
        """
        return self.read_input_registers(self.addresses.gateway_device_id, 0, 1)[0]

    def message_registers(self):
        """
        Read pending messages stored into the gateway.

        Note
        -----
        Once a message is read, it is deleted inside the *Xcom-485i*, so use `Xcom485i.pending_message_count` in order
        to know how many messages are pending and iteratively call this function to retrieve all messages.

        The response is like :\n
        - Input Register 0 (@ 0x0001)| 2 bytes | Device source\n
        - Input Register 1 (@ 0x0002)| 2 bytes | Message ID\n
        - Input Register 2 (@ 0x0003)| 2 bytes | Optional value Most significant word\n
        - Input Register 3 (@ 0x0004)| 2 bytes | Optional value Least significant word\n

        Returns
        -------
        bytes
            Content of Input Register 0, 1, 2, 3

        Example
        --------
        .. code-block:: python

            # Read all pending messages stored into the gateway
            # Run this example within the 'examples/' folder using 'python ex_read_messages.py' from a CLI
            #   after installing xcom485i package with 'pip install xcom485i'

            import serial
            from xcom485i.client import Xcom485i

            SERIAL_PORT_NAME = 'COM4'  # your serial port interface name
            SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
            DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

            if __name__ == "__main__":
                try:
                    serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE,
                                                parity=serial.PARITY_EVEN, timeout=1)
                except serial.serialutil.SerialException as e:
                    print("Check your serial configuration : ", e)
                else:
                    xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=True)
                    # always check the number of pending messages
                    pending_message_count = xcom485i.pending_message_count()
                    print('pending_message_count:', pending_message_count)

                    for _ in range(pending_message_count):
                        message_registers = xcom485i.message_registers()
                        print('Message N°:', _)
                        print("\t device source: ", message_registers[0])
                        print("\t message id: ", message_registers[1])
                        print("\t optionnal most significant word: ", message_registers[2])
                        print("\t optionnal least significant word: ", message_registers[3])
        """
        return self.read_input_registers(self.addresses.gateway_device_id, 1, 4)
