#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import os
import cantools

# Import certain classes and methods from libraries
from flask import send_from_directory
from dash.dependencies import Input, Output
from panda import Panda
from os.path import dirname, abspath, join


# Create the app and assign excepctions
app = dash.Dash()
app.title = 'GAP AND SPEED VISUALIZATION'
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
PANDA = Panda()
PANDA.can_clear(0xFFFF)
PANDA.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
# Send request to broadcast leddar messages
dat = '0301000000000000'
PANDA.can_send(0x740, dat.decode('hex'), 1)

# DBC files: car and leddar
base_path = dirname(abspath(__file__))
leddar = join(base_path,'dbc_files/leddar_vu_8_segments.dbc')
car = join(base_path,'dbc_files/ford_fusion_2011.dbc')
CAR_DBC = cantools.database.load_file(car)
LEDDAR_DBC = cantools.database.load_file(leddar)
CAN_VARIABLES = []


# Layout of the app
app.layout = html.Div([ 

    html.Link(
        rel='stylesheet',
        href='/static/stylesheet.css'
    ),
            
    dcc.Interval(
        id = 'refresh',
        interval = 100,
        n_intervals = 0
    ),
            
    # This is an auxiliar division to read CAN
    html.Div(id='read_can'),
            
    html.Div([

        html.Div([
            html.Div([
                html.Label('Target Speed (MPH):',
                    style = {'fontSize': 20},
                )
            ], className = 'row'),
            html.Div([
                dcc.Input(
                    placeholder = 'Enter a target speed...',
                    type = 'number',
                    id = 'speed_input',
                ),  
            ], className = 'row'),  
            html.Div([
                html.Div([
                    daq.Tank(
                        id = 'target_speed_tank',
                        value = 0,
                        min = 0,
                        max = 100,
                        showCurrentValue = True,
                        color = 'lightgreen',
                        label = 'Target speed',
#                        style={'margin-left': '40px',
#                               'margin-top': '10px'}
                    ),
                ], className = 'two columns'),    
                html.Div([
                    daq.Tank(
                        id = 'speed_tank',
                        value = 0,
                        min = 0,
                        max = 100,
                        showCurrentValue = True,
                        label = 'Speed',
#                        style={'margin-left': '40px',
#                               'margin-top': '10px'}
                    ),
                ], className = 'two columns'),            
            ], className = 'row')
        ], className = 'five columns'),
    
        html.Div([
            html.Div([
                html.Label('Target Gap (m):',
                    style = {'fontSize': 20},
                )
            ], className = 'row'),
            html.Div([
                dcc.Input(
                    placeholder = 'Enter a target gap...',
                    type = 'number',
                    id = 'gap_input',
                ),  
            ], className = 'row'),  
            html.Div([
                html.Div([
                    daq.Tank(
                        id = 'target_gap_tank',
                        value = 0,
                        min = 0,
                        max = 100,
                        label = 'Target gap',
                        color = 'lightgreen',
                        showCurrentValue = True,
#                        style={'margin-left': '40px',
#                               'margin-top': '10px'}
                    ),
                ], className = 'two columns'),      
                html.Div([
                    daq.Tank(
                        id = 'gap_tank',
                        value = 0,
                        min = 0,
                        max = 100,
                        label = 'Gap',
                        showCurrentValue = True,
#                        style={'margin-left': '40px',
#                               'margin-top': '10px'}
                    ),
                ], className = 'two columns'), 
            ], className = 'row')
        ], className = 'five columns'),    
            
    ], className = 'row')

             
])
    
    
@app.callback(
     Output('target_speed_tank', 'value'),
    [Input('speed_input', 'value')])
def show_target_speed(target_speed):
	return target_speed


@app.callback(
     Output('target_gap_tank', 'value'),
    [Input('gap_input', 'value')])
def show_target_gap(target_gap):
	return target_gap


@app.callback(
     Output('read_can', 'value'),
    [Input('refresh', 'n_intervals')])
def read_can(n):
	global CAR_DBC, LEDDAR_DBC, CAN_VARIABLES, PANDA
	
	can_recv = []
	can_recv = PANDA.can_recv()
	CAN_VARIABLES = [0,0]
	speed, gap = 0, 0
	
	if can_recv != []:
		for address, _, dat, _  in can_recv:
			if address == 0x215:
				msg = CAR_DBC.decode_message(address, dat)
				speed = (msg['Veh_wheel_speed_RR_CAN_kph_'] +
						  msg['Veh_wheel_speed_FL_CAN_kph_'] + 
						  msg['Veh_wheel_speed_RL_CAN_kph_'] +
						  msg['Veh_wheel_speed_FR_CAN_kph_'])*0.25*0.62137119
				CAN_VARIABLES[0] = speed
			elif (address == 0x752 or address == 0x753 or address == 0x754 or
				address == 0x755 or address == 0x756 or address == 0x757 or
				address == 0x758 or address == 0x759):
				msg = LEDDAR_DBC.decode_message(address, dat)
				if msg['lidar_channel'] == 4:
					gap = msg['lidar_distance_m'] 
					CAN_VARIABLES[1] = gap
                               
@app.callback(
     Output('speed_tank', 'value'),
    [Input('refresh', 'n_intervals')])
def show_speed(n):
	return CAN_VARIABLES[0]

@app.callback(
     Output('gap_tank', 'value'),
    [Input('refresh', 'n_intervals')])
def show_gap(n):
	return CAN_VARIABLES[1]                    
    
    
# Run the app in local server
if __name__ == '__main__':
    app.run_server(debug=False)