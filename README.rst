Package **xcom485i**
=========================

Python library to access Studer-Innotec Xcom-485i device through Modbus RTU over a serial port

Prerequisites
----------------

Please read the complete documentation available on : `Studer Innotec SA`_ *-> Support -> Download Center -> Software and Updates -> Communication protocols Xcom-CAN*

Getting Started
----------------

1. Package installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ pip install xcom485i

2. Hardware installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Connect your *Xcom-485i* (Studer side) to your installation using the cable provided with the device
- Connect your *Xcom-485i* (External side) to your controller (personal computer, Raspberry Pi, etc.) using a *USB* to *RS-485* adapter
- Please refer to the *Xcom-485i* manual for more information about commissioning the device

3. Serial configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This package rely on `pyserial`_ standard package, in order to use the **xcom485i** package make sure to instantiate it like :

.. code-block:: python

    import serial

    serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE, parity=serial.PARITY_EVEN, timeout=1)

- where `SERIAL_PORT_NAME` is your serial port interface, for example set it to *'COM4'* (string argument) when using *Windows* otherwise you may set it to *'/dev/ttyUSB0/'* on *Linux*
- where `SERIAL_PORT_BAUDRATE` is the baudrate used by your serial port interface (must be set to 9600, 19200, 38400 or 115200 according to *Xcom-485i* dip-switches)

**Xcom-485i Dip switches baud rate selection**

=====   =====   ===========
N° 7    N° 8    Baudrate
=====   =====   ===========
OFF     OFF     9600   bps
OFF     ON      19200  bps
ON      OFF     38400  bps
ON      ON      115200 bps
=====   =====   ===========

4. Address offset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the modbus offset corresponding to the internal dip-switches of your *Xcom-485i* device, it must be set to 0, 32, 64 or 128.

It is done when instantiate the *Xcom485i* class like :

.. code-block:: python

    xcom485i = Xcom485i(serial_port, OFFSET, debug=True)

- where `serial_port` is the previously created object with *Serial*
- where `OFFSET` is your actual modbus address offset set by the dip-switches inside your *Xcom-485i*
- where `debug` enables you to get some useful console information for debugging purpose

**Xcom-485i Dip switches address offset selection**

=====   =====   ===============   ==============
N° 1    N° 2    Address offset    Address range
=====   =====   ===============   ==============
OFF     OFF     0                 1 to 63
OFF     ON      32                33 to 95
ON      OFF     64                65 to 127
ON      ON      128               129 to 192
=====   =====   ===============   ==============

5. Run an example from `/examples` folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to */examples* folder with a terminal and execute this script

.. code-block:: console

    $ python ex_read_info.py

Check `client file`_ to understand it.

6. Open documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open documentation from `Read The Docs`_

Warnings
----------------

- **Please** check carefully the serial configuration, the *Xcom-485i* dip-switches configuration as well as the jumper for D+, D- and GND signals
- **Use** devices addresses generated into `addresses file`_
- It is strongly recommended **NOT** to spam the *Xcom-485i* with multiple requests. The correct way to communicate with the *Xcom-485i* is to send a request and to **wait** for the response before sending the next request. If no response comes from the *Xcom-485i* after a delay of 1 second, we can consider that the timeout is over and another request can be send. It is also how *Modbus RTU* is intended to work.

Authors
----------------

**Studer Innotec SA** - *Initial work* - `Studer Innotec SA`_

License
----------------

This project is licensed under the MIT License - see the `LICENSE`_ file for details

.. External References:
.. _Studer Innotec SA: https://www.studer-innotec.com
.. _addresses file: https://xcom485i.readthedocs.io/en/latest/addresses.html
.. _client file: https://xcom485i.readthedocs.io/en/latest/client.html
.. _Read The Docs: https://xcom485i.readthedocs.io/en/latest/index.html
.. _LICENSE: https://xcom485i.readthedocs.io/en/latest/license.html
.. _pyserial: https://pyserial.readthedocs.io/en/latest/shortintro.html
