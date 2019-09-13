#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cantools

# Import certain classes and methods from libraries
from flask import send_from_directory
from dash.dependencies import Input, Output
from panda import Panda
from os.path import dirname, abspath, join

# DBC files: car and leddar
base_path = dirname(abspath(__file__))
parent_path = abspath(join(base_path, os.pardir))

# Create the app and assign excepctions
app = dash.Dash()
app.title = 'CHECK LIDAR DISTANCE - CALIBRATION'
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
parent_path = abspath(join(base_path, os.pardir))
leddar = join(parent_path,'dbc_files/leddar_vu_8_segments.dbc')
LEDDAR_DBC = cantools.database.load_file(leddar)

# Layout of the app
app.layout = html.Div([

    html.Link(
        rel='stylesheet',
        href='/static/stylesheet.css'
    ),

    dcc.Interval(
        id = 'refresh',
        interval = 200,
        n_intervals = 0
    ),
            
    html.Div([
        html.Div([
            html.Label('Gap (m):',
                style = {'color': '#262626',
                         'fontSize': 40},
            )
        ], className = 'row', style={'padding': 5}),
        html.H1(id='display_gap',
                style = {'color': '#262626',
                         'fontSize': 140})            
    ], className = 'row', style = {'textAlign': 'center'})

  
])
    
    
@app.callback(
     Output('display_gap', 'children'),
    [Input('refresh', 'n_intervals')])
def display_gap(gap):
    can_recv = []
    can_recv = PANDA.can_recv()
    
    if can_recv != []:
        for address, _, dat, _  in can_recv:
            if (address == 0x752 or address == 0x753 or address == 0x754 or
    		    	address == 0x755 or address == 0x756 or address == 0x757 or
				    address == 0x758 or address == 0x759):
                msg = LEDDAR_DBC.decode_message(address, dat)
                if msg['lidar_channel'] == 4:
                    # Clear the buffer of the CAN buses that we use
                    PANDA.can_clear(0xFFFF)
                    return msg['lidar_distance_m']
    else:
        return '-'


# Run the app in local server
if __name__ == '__main__':
    app.run_server(debug=False)