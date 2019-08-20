#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import binascii
import sys
import time
import cantools
import pandas as pd
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt

# Import certain classes and methods from libraries
from panda import Panda
from datetime import datetime
from os.path import dirname, abspath, join
from nidaqmx.constants import TerminalConfiguration

# Import classes, methods, and functions from custom libraries
from gps_ublox.gps import lat_longitude_from_serial
from resources import get_nidaqmx_dev_name

def can_logger(car_dbc = None, leddar_dbc = None, port = None,
               sample_time = 0.2, filename = None):

    try:
        print("Trying to connect to Panda over USB...")
        if port != None:
            p = Panda(port)
        else:
            p = Panda() # default port
        p.can_clear(0xFFFF)
        print('Buffer cleaned')
        # Send leddar request to start transmitting - Read LeddarVu 8 documentation
        p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
        dat = '0301000000000000'
        p.can_send(0x740, dat.decode('hex'), 1)
        p.serial_clear(1)

    except AssertionError:
        print("USB connection failed. Trying WiFi...")
        try:
            p = Panda("WIFI")
        except:
            print("WiFi connection timed out. Please make sure\
                  your Panda is connected and try again.")
            sys.exit(0)

    try:
        columns = ['time_rel',
                   'timestamp',
                   'vehicle_speed_mph',
                   'eng_speed_rpm',
                   'pedal_per',
                   'gap_m',
                   'latitude_deg',
                   'longitude_deg',
                   'axle_torque_ch_0_V',
                   'axle_torque_ch_1_V']

        df = pd.DataFrame(columns = columns)
        rel_time = 0
        dt = sample_time
        device = get_nidaqmx_dev_name()

        while True:
            time.sleep(dt)
            row = {}
            row[columns[0]] = rel_time
            row[columns[1]] = str(datetime.now())
            can_recv = p.can_recv()
            gps = p.serial_read(1)
            for address, _, dat, _  in can_recv:
                if address == 0x215:
                    msg = car_dbc.decode_message(address, dat)
                    row[columns[2]] = (msg['Veh_wheel_speed_RR_CAN_kph_'] +
                                       msg['Veh_wheel_speed_FL_CAN_kph_'] +
                                       msg['Veh_wheel_speed_RL_CAN_kph_'] +
                                       msg['Veh_wheel_speed_FR_CAN_kph_'])*0.25*0.62137119
                elif address == 0x201:
                    msg = car_dbc.decode_message(address, dat)
                    row[columns[3]] = msg['Eng_speed_CAN_rpm_']
                    row[columns[4]] = msg['Pedal_accel_pos_CAN_per_']
                elif (address == 0x752 or address == 0x753 or
                      address == 0x754 or address == 0x755 or
                      address == 0x756 or address == 0x757 or
                      address == 0x758 or address == 0x759):
                    msg = leddar_dbc.decode_message(address, dat)
                    if msg['lidar_channel'] == 4:
                        row[columns[5]] = msg['lidar_distance_m']
            # Clear the CAN bus to avoid the buffer
            p.can_clear(0xFFFF)

            lat, long = lat_longitude_from_serial(gps)
            row[columns[6]] = lat
            row[columns[7]] = long
             # Add nidaqmx channels
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(device + "/ai0", terminal_config = TerminalConfiguration.RSE)
                task.ai_channels.add_ai_voltage_chan(device + "/ai1", terminal_config = TerminalConfiguration.RSE)
                analog_channels = np.array(task.read(number_of_samples_per_channel=100)).mean(axis = 1)
            row[columns[8]] = analog_channels[0]
            row[columns[9]] = analog_channels[1]
            print(row)
            df = df.append(row, ignore_index = True)
            rel_time += dt

    except KeyboardInterrupt:
        if filename == None:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + 'output.csv'
        else:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + filename + '.csv'
        df.to_csv(filename, index = False)

        # Print and plot results in the screen
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(df['time_rel'], df['gap_m'])
        plt.ylabel('gap (m)')
        plt.subplot(2,1,2)
        plt.plot(df['time_rel'], df['axle_torque_ch_0_V'])
        plt.plot(df['time_rel'], df['axle_torque_ch_1_V'])
        plt.ylabel('torque voltages')
        plt.xlabel('time (sec)')
        plt.legend()
        plt.show()

if __name__ == "__main__":

    # Read dbc files and loaded into the can_logger_function
    base_path = dirname(abspath(__file__))
    leddar = join(base_path,'dbc_files/leddar_vu_8_segments.dbc')
    car = join(base_path,'dbc_files/ford_fusion_2011.dbc')

    leddar_dbc = cantools.database.load_file(leddar)
    car_dbc = cantools.database.load_file(car)
    # port_send = '53002c000c51363338383037'
    # port_recv = '240050000c51363338383037'
    can_logger(car_dbc = car_dbc, leddar_dbc = leddar_dbc, sample_time = 0.2)
