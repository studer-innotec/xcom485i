#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WARNINGS
-----------
This file **MUST NOT** be edited.

Please read the complete documentation available on : `Studer Innotec SA <https://www.studer-innotec.com>`_ *-> Support -> Download Center -> Software and Updates -> Communication protocols Xcom-CAN*

!!! DO NOT CHANGE CONFIGURATIONS BELOW !!!
"""


class Addresses:
    """
    This class stores all accessible addresses from the Xcom485i device

    Attributes
    ----------
    dip_switches_offset
        The address offset as defined with the dip-switches into the device
    gateway_device_id
        Xcom-485i Modbus gateway address for configuration and status
    system_device_id
        Xcom-485i Modbus system address for configuration and status
    xt_group_device_id
        Virtual address to access all XTH, XTM and XTS (Multicast)
    xt_l1_group_device_id
        Virtual address to access all XTH, XTM and XTS (Multicast) present on the same phase, in this case L1
    xt_1_device_id
        First Xtender device address, up to 9 XT allowed, ordered by the index displayed on the RCC (Unicast)
    vt_group_device_id
        Virtual address to access all VarioTrack (Multicast)
    vt_1_device_id
        First VarioTrack device address, up to 15 VarioTrack allowed, ordered by the index displayed on the RCC
        (Unicast)
    vs_group_device_id
        Virtual address to access all VarioString (Multicast)
    vs_1_device_id
        First VarioString device address, up to 15 VarioString allowed, ordered by the index displayed on the RCC
        (Unicast)
    bsp_group_device_id
        Virtual address to access the BSP or the Xcom-CAN BMS (Multicast)
    bsp_device_id
        A single BSP or Xcom-CAN BMS (Unicast)
    read_param_flash_offset
        Offset to read a parameter from flash
    read_param_min_offset
        Offset to read the minimum parameter value from flash
    read_param_max_offset
        Offset to read the maximal parameter value from flash
    write_param_flash_ram
        Offset to write a parameter into flash and ram
    write_param_ram_only
        Offset to write a parameter into ram only
    """

    def __init__(self, offset):
        self.dip_switches_offset = offset
        self.gateway_device_id = self.dip_switches_offset + 1
        self.system_device_id = self.dip_switches_offset + 2

        self.xt_l1_group_device_id = self.dip_switches_offset + 7
        self.xt_l2_group_device_id = self.dip_switches_offset + 8
        self.xt_l3_group_device_id = self.dip_switches_offset + 9
        self.xt_group_device_id = self.dip_switches_offset + 10
        self.xt_1_device_id = self.xt_group_device_id + 1
        self.xt_2_device_id = self.xt_group_device_id + 2
        self.xt_3_device_id = self.xt_group_device_id + 3
        self.xt_4_device_id = self.xt_group_device_id + 4
        self.xt_5_device_id = self.xt_group_device_id + 5
        self.xt_6_device_id = self.xt_group_device_id + 6
        self.xt_7_device_id = self.xt_group_device_id + 7
        self.xt_8_device_id = self.xt_group_device_id + 8
        self.xt_9_device_id = self.xt_group_device_id + 9

        self.vt_group_device_id = self.dip_switches_offset + 20
        self.vt_1_device_id = self.vt_group_device_id + 1
        self.vt_2_device_id = self.vt_group_device_id + 2
        self.vt_3_device_id = self.vt_group_device_id + 3
        self.vt_4_device_id = self.vt_group_device_id + 4
        self.vt_5_device_id = self.vt_group_device_id + 5
        self.vt_6_device_id = self.vt_group_device_id + 6
        self.vt_7_device_id = self.vt_group_device_id + 7
        self.vt_8_device_id = self.vt_group_device_id + 8
        self.vt_9_device_id = self.vt_group_device_id + 9
        self.vt_10_device_id = self.vt_group_device_id + 10
        self.vt_11_device_id = self.vt_group_device_id + 11
        self.vt_12_device_id = self.vt_group_device_id + 12
        self.vt_13_device_id = self.vt_group_device_id + 13
        self.vt_14_device_id = self.vt_group_device_id + 14
        self.vt_15_device_id = self.vt_group_device_id + 15

        self.vs_group_device_id = self.dip_switches_offset + 40
        self.vs_1_device_id = self.vs_group_device_id + 1
        self.vs_2_device_id = self.vs_group_device_id + 2
        self.vs_3_device_id = self.vs_group_device_id + 3
        self.vs_4_device_id = self.vs_group_device_id + 4
        self.vs_5_device_id = self.vs_group_device_id + 5
        self.vs_6_device_id = self.vs_group_device_id + 6
        self.vs_7_device_id = self.vs_group_device_id + 7
        self.vs_8_device_id = self.vs_group_device_id + 8
        self.vs_9_device_id = self.vs_group_device_id + 9
        self.vs_10_device_id = self.vs_group_device_id + 10
        self.vs_11_device_id = self.vs_group_device_id + 11
        self.vs_12_device_id = self.vs_group_device_id + 12
        self.vs_13_device_id = self.vs_group_device_id + 13
        self.vs_14_device_id = self.vs_group_device_id + 14
        self.vs_15_device_id = self.vs_group_device_id + 15

        self.bsp_group_device_id = self.dip_switches_offset + 60
        self.bsp_device_id = self.bsp_group_device_id + 1

        self.read_param_flash_offset = 0
        self.read_param_min_offset = 2000
        self.read_param_max_offset = 4000
        self.write_param_flash_ram = 0
        self.write_param_ram_only = 6000
