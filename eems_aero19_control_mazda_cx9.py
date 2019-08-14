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
#from panda import Panda
from os.path import dirname, abspath, join
from datetime import datetime

# Import classes, methods, and functions from custom libraries
from resources import get_panda_id
from static import app_layouts
from pedal_models.pedal_vs_speed_accel import PedalModel as PM
from resources import get_nidaqmx_dev_name

# Create the app and assign excepctions
app = dash.Dash()
app.title = 'GAP AND SPEED CONTROL AND VISUALIZATION'
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
#panda_port = get_panda_id('mazda_cx9', 'send')
#PANDA = Panda(panda_port)
#PANDA.can_clear(0xFFFF)
#PANDA.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
## Send request to broadcast leddar messages
#dat = '0301000000000000'
#PANDA.can_send(0x740, dat.decode('hex'), 1)

# DBC files: car and leddar
base_path = dirname(abspath(__file__))
leddar = join(base_path,'dbc_files/leddar_vu_8_segments.dbc')
car = join(base_path,'dbc_files/mazda_cx9_2016.dbc')
CAR_DBC = cantools.database.load_file(car)
LEDDAR_DBC = cantools.database.load_file(leddar)
CAN_VARIABLES = []
PEDAL_MODEL = PM('mazda_cx9')
#DEV = get_nidaqmx_dev_name()
X = []
Y0 = []; Y1 = []; Y2 = []; Y3 = []
TRACES0 = []; TRACES1 = []; TRACES2 = []; TRACES3 = []

# Layout of the app
app.layout = app_layouts.layout_control

@app.callback(
     Output('live_update_graph', 'figure'),
    [Input('refresh', 'n_intervals'),
	  Input('gap_input', 'value'),
     Input('speed_input', 'value')])
def update_figure_send_controls(n, target_gap, target_speed):

    X.append(datetime.now())
    Y0.append(target_gap)
    Y1.append(target_speed)

    if len(X) >= 100:
        X.pop(0)
        Y0.pop(0)
        Y1.pop(0)

    TRACES0 = go.Scatter(
        x = X,
        y = Y0,
        mode = 'lines+markers',
        name = 'target_gap'
	)
    TRACES1 = go.Scatter(
        x = X,
        y = Y1,
        mode = 'lines+markers',
        name = 'target_speed'
	)
    return {
		'data': [TRACES0, TRACES1]
	}

#@app.callback(
#     Output('read_can', 'value'),
#    [Input('refresh', 'n_intervals')])
#def read_can(n):
#	global CAR_DBC, LEDDAR_DBC, CAN_VARIABLES, PANDA
#
#	can_recv = []
#	can_recv = PANDA.can_recv()
#	CAN_VARIABLES = [0,0]
#	speed, gap = 0, 0
#
#	if can_recv != []:
#		for address, _, dat, _  in can_recv:
#			if address == 0x215:
#				msg = CAR_DBC.decode_message(address, dat)
#				speed = (msg['Veh_wheel_speed_RR_CAN_kph_'] +
#						  msg['Veh_wheel_speed_FL_CAN_kph_'] +
#						  msg['Veh_wheel_speed_RL_CAN_kph_'] +
#						  msg['Veh_wheel_speed_FR_CAN_kph_'])*0.25*0.62137119
#				CAN_VARIABLES[0] = speed
#			elif (address == 0x752 or address == 0x753 or address == 0x754 or
#				address == 0x755 or address == 0x756 or address == 0x757 or
#				address == 0x758 or address == 0x759):
#				msg = LEDDAR_DBC.decode_message(address, dat)
#				if msg['lidar_channel'] == 4:
#					gap = msg['lidar_distance_m']
#					CAN_VARIABLES[1] = gap


# Run the app in local server
if __name__ == '__main__':
    app.run_server(debug=False)



