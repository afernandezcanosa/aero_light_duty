#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import os
import cantools
import plotly.graph_objs as go

# Import certain classes and methods from libraries
from flask import send_from_directory
from dash.dependencies import Input, Output
from panda import Panda
from os.path import dirname, abspath, join
from datetime import datetime
import nidaqmx

# Import classes, methods, and functions from custom libraries
from static import app_layouts
from pedal_models.pedal_vs_speed_accel import PedalModel as PM
from resources import get_nidaqmx_dev_name, get_panda_id, visualization_props

# Create the app and assign excepctions
app = dash.Dash()
app.title = 'SPEED CONTROL AND VISUALIZATION'
app.config['suppress_callback_exceptions']=True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Boostrap CSS file (local)
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

# Global variables and initialization
# Open panda device (comma ai) and clear the buffer
panda_port = get_panda_id('mazda_cx9', 'send')
PANDA = Panda(panda_port)
PANDA.can_clear(0xFFFF)
PANDA.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
# Send request to broadcast leddar messages
dat = '0301000000000000'
PANDA.can_send(0x740, dat.decode('hex'), 1)

# DBC files: car and leddar
base_path = dirname(abspath(__file__))
leddar = join(base_path,'dbc_files/leddar_vu_8_segments.dbc')
car = join(base_path,'dbc_files/mazda_cx9_2016.dbc')
CAR_DBC = cantools.database.load_file(car)
LEDDAR_DBC = cantools.database.load_file(leddar)
SPEED = 0
PEDAL_MODEL = PM('mazda_cx9')
DEV = get_nidaqmx_dev_name()
PROPS_VIS = visualization_props()
X = []
Y0 = []; Y1 = []
TRACES0 = []; TRACES1 = []

# Layout of the app
app.layout = app_layouts.layout_control_cruise_control(PROPS_VIS)

@app.callback(
     Output('live_update_graph', 'figure'),
    [Input('refresh', 'n_intervals'),
      Input('speed_input', 'value'),
      Input('prop_gain', 'value'),
      Input('max_accel', 'value'),
      Input('min_accel', 'value')])
def update_figure_send_controls(n, target_speed, kp, max_accel, min_accel):
    global SPEED

    X.append(datetime.now())
    Y0.append(target_speed)
    Y1.append(SPEED)

    # Control Input
    a_control = kp*(target_speed - SPEED)*0.44704

    if a_control > max_accel:
        a_control = max_accel
    elif a_control < min_accel:
        a_control = min_accel

    # Acceleration pedal input
    accel_pedal_per = PEDAL_MODEL.pedal_per(SPEED*0.44704, a_control)

    # Send the voltages
    v0, v1 = PEDAL_MODEL.voltage_from_pedal(accel_pedal_per)
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(DEV + "/ao0")
        task.ao_channels.add_ao_voltage_chan(DEV + "/ao1")
        task.write([v0, v1], auto_start=True)

    if len(X) >= PROPS_VIS['points_per_plot']:
        X.pop(0)
        Y0.pop(0)
        Y1.pop(0)

    TRACES0 = go.Scatter(
        x = X,
        y = Y0,
        mode = 'lines+markers',
        name = 'target_speed_mph'
	)
    TRACES1 = go.Scatter(
        x = X,
        y = Y1,
        mode = 'lines+markers',
        name = 'real_speed_mph'
	)
    return {
		'data': [TRACES0, TRACES1]
	}

@app.callback(
     Output('read_can', 'value'),
    [Input('refresh', 'n_intervals')])
def read_can(n):
	global CAR_DBC, LEDDAR_DBC, CAN_VARIABLES, PANDA, SPEED

	can_recv = []
	can_recv = PANDA.can_recv()

	if can_recv != []:
		for address, _, dat, _  in can_recv:
			if address == 0x215:
				msg = CAR_DBC.decode_message(address, dat)
				speed = (msg['Veh_wheel_speed_RR_CAN_kph_'] +
						  msg['Veh_wheel_speed_FL_CAN_kph_'] +
						  msg['Veh_wheel_speed_RL_CAN_kph_'] +
						  msg['Veh_wheel_speed_FR_CAN_kph_'])*0.25*0.62137119
				SPEED = speed
        # Clear the buffer of the CAN buses that we use
        PANDA.can_clear(0xFFFF)

# Run the app in local server
if __name__ == '__main__':
    app.run_server(debug=False)
