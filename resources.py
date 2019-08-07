#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import nidaqmx

def get_nidaqmx_dev_name():
    system = nidaqmx.system.System.local()
    device = system.devices[0]
    return device.name


if __name__ == "__main__":
    device = get_nidaqmx_dev_name()
    print(device)
