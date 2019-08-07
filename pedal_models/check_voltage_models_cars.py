#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cantools
import nidaqmx
import plotly.graph_objs as go

# Import certain classes and methods from libraries
from flask import send_from_directory
from dash.dependencies import Input, Output
from panda import Panda
from os.path import dirname, abspath, join
from datetime import datetime

# Import local libraries
from pedal_vs_speed_accel import PedalModel as PM
from resources import get_nidaqmx_dev_name


# Create the app and assign excepctions
app = dash.Dash()
app.title = 'CHECK VOLTAGE-PEDAL MODELS'
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
X = []
Y0 = []; Y1 = []
TRACES0 = []; TRACES1 = []

# DBC files: car and leddar
base_path = dirname(abspath(__file__))
parent_path = abspath(join(base_path, os.pardir))
DBC_FILE = None
VOLTAGE_MODEL = None
DEV = get_nidaqmx_dev_name()


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

    # Aux to store the car model
    html.Div(id='store_car'),

    html.Div([
        html.Div([
            html.Label('CAR MODEL:',
                       style = {
                           'textAlign': 'right',
                           'fontSize': 20,
                           'fontWeight': 'bold',
                           'position': 'relative',
                           'padding-top': 3
                       }
            )
        ], className = 'three columns'),

        html.Div([
            dcc.Dropdown(
                id='car_dropdown',
                options=[
                    {'label': 'mazda_cx9', 'value': 'mazda_cx9'},
                    {'label': 'ford_f150', 'value': 'ford_f150'},
                    {'label': 'ford_fusion', 'value': 'ford_fusion'}
                ],
                style = {'width': 900},
                value='mazda_cx9'
                ),
        ], className = 'nine columns'),
    ], className = 'row', style={'padding': 20}),

    html.Div([
        html.Div([
            html.Label('PEDAL INPUT:',
                       style = {
                           'textAlign': 'right',
                           'fontSize': 20,
                           'fontWeight': 'bold',
                           'position': 'relative',
                           'padding-top': 3
                       }
            )
        ], className = 'three columns'),

        html.Div([
            daq.Slider(
                id = 'pedal_input',
                min = 0,
                max = 100,
                step = 1,
                value = 0,
                size = 900,
                updatemode = 'drag',
                marks={i: '{}'.format(i) for i in range(0,101,10)},
            )
        ], className = 'nine columns'),
    ], className = 'row', style={'padding': 20}),

    html.Div([
        dcc.Graph(id='live_update_graph'),
    ], className = 'row', style={'padding': 20})
])


@app.callback(
     Output('store_car', 'value'),
    [Input('car_dropdown', 'value')])
def read_can(car_name):
    global DBC_FILE, VOLTAGE_MODEL
    if car_name == 'mazda_cx9':
        car = join(parent_path,'dbc_files\\' + car_name + '_2016.dbc')
    elif car_name == 'ford_f150':
        car = join(parent_path,'dbc_files\\' + car_name + '_2017.dbc')
    elif car_name == 'ford_fusion':
        car = join(parent_path,'dbc_files\\' + car_name + '_2011.dbc')

    DBC_FILE = cantools.database.load_file(car)
    VOLTAGE_MODEL = PM(car_name)


@app.callback(
     Output('live_update_graph', 'figure'),
    [Input('refresh', 'n_intervals'),
	 Input('pedal_input', 'value'),
    Input('car_dropdown', 'value')])
def real_gas(n, pedal_input, car):

    global DBC_FILE, VOLTAGE_MODEL, PANDA

    v0, v1 = VOLTAGE_MODEL.voltage_from_pedal(pedal_input)

    real_pedal = 0

    can_recv = PANDA.can_recv()
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(DEV + "/ao0")
        task.ao_channels.add_ao_voltage_chan(DEV + "/ao1")
        task.write([v0, v1], auto_start=True)

    if car == 'mazda_cx9':
        for address, _, dat, _ in can_recv:
            if address == 0x167:
                msg = DBC_FILE.decode_message(address, dat)
                real_pedal = msg['Pedal_accel_pos_CAN_per_']
                break

    elif car == 'ford_f150':
        for address, _, dat, _ in can_recv:
            if address == 0x204:
                msg = DBC_FILE.decode_message(address, dat)
                real_pedal = msg['Pedal_accel_pos_CAN_per_']
                break

    elif car == 'ford_fusion':
        for address, _, dat, _ in can_recv:
            if address == 0x201:
                msg = DBC_FILE.decode_message(address, dat)
                real_pedal = msg['Pedal_accel_pos_CAN_per_']
                break

    X.append(datetime.now())
    Y0.append(pedal_input)
    Y1.append(real_pedal)

    if len(X) >= 100:
        X.pop(0)
        Y0.pop(0)
        Y1.pop(0)

    TRACES0 = go.Scatter(
        x = X,
        y = Y0,
        mode = 'lines+markers',
        name = 'input_pedal'
	)
    TRACES1 = go.Scatter(
        x = X,
        y = Y1,
        mode = 'lines+markers',
        name = 'real_pedal'
	)
    return {
		'data': [TRACES0, TRACES1]
	}


# Run the app in local server
if __name__ == '__main__':
    app.run_server(debug=False)
