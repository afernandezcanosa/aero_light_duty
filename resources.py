#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import nidaqmx

def get_nidaqmx_dev_name():
    system = nidaqmx.system.System.local()
    device = system.devices[0]
    return device.name

def get_panda_id(car_name, option):
    if car_name == 'mazda_cx9':
        if option == 'recv':
            return '53002c000c51363338383037'
        elif option == 'send':
            return '4e0046000651363038363036'
        else:
            raise ValueError("Please introduce a valid option: recv - send")
    elif car_name == 'ford_f150':
        if option == 'recv':
            return '360024000c51363338383037'
        elif option == 'send':
            return '26003f000651363038363036'
        else:
            raise ValueError("Please introduce a valid option: recv - send")
    elif car_name == 'ford_fusion':
        if option == 'recv':
            return '240050000c51363338383037'
        elif option == 'send':
            return '540041000651363038363036'
        else:
            raise ValueError("Please introduce a valid option: recv - send")
    else:
        raise ValueError("Please introduce a valid vehicle")


def can_recv_to_dict(can_recv):
	# Convert to dictionary
	can_recv_dict = {}
	for address, _, dat, _  in can_recv:
		can_recv_dict[address] = dat

	return can_recv_dict

def visualization_props():
    " Specifies generic properties of the real-time dash visualizations "
    props = {}
    props['points_per_plot'] = 25
    props['refresh_rate'] = 200 # miliseconds

    # Maximum and minimum acceleration rates
    props['max_accel'] = 0.8 # m/s^2
    props['min_accel'] = -0.8 # m/s^2

    # Gains of the controllers (tuned in Navistar tests 08-22-2019)
    props['Kp_conv_cruise'] = 0.4 # Conventional cruise control
    props['Kp'] = 0.10 # Gap control prop gain
    props['Kd'] = 0.35 # Gap control der gain

    return props

if __name__ == "__main__":
    device = get_nidaqmx_dev_name()
    print(device)
