#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

def layout_viz():
    return  html.Div([
                html.Div([
                    html.H1('EEMS Aero - Visualization display')
                ], className = 'row'),

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
                        ], className = 'row', style={'padding': 20}),
                        html.Div([
                            dcc.Graph(id='speed_graph',
                                      figure={
                                          'data': [go.Bar(x=[0, 0],
                                                          y=['Target', 'Real'],
                                                          marker_color = ['red', 'indianred'],
                                                          orientation='h')],
                                            }
                                        ),
                        ], className = 'row', style={'padding': 20})
                    ], className = 'six columns'),

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
                        ], className = 'row', style={'padding': 20}),
                        html.Div([
                            dcc.Graph(id='gap_graph',
                                      figure={
                                          'data': [go.Bar(x=[0, 0],
                                                          y=['Target', 'Real'],
                                                          marker_color = ['red', 'indianred'],
                                                          orientation='h')],
                                            }
                                        ),
                        ], className = 'row', style={'padding': 20})
                    ], className = 'six columns'),
                ], className = 'row')
            ])

def layout_control():

    colors = {
        'background': '#c2f0c2',
        'text': '#248f24'
    }

    return  html.Div(style = {'backgroundColor': colors['background']}, children =[
                html.Div([
                    html.H1(
                            children = 'EEMS Aero 2019 - Pedal control display',
                            style = {'color': colors['text']}
                    ),
                ], className = 'row', style={'padding': 10}),

                dcc.Interval(
                    id = 'refresh',
                    interval = 100,
                    n_intervals = 0
                ),

                html.Link(
                    rel='stylesheet',
                    href='/static/stylesheet.css'
                ),

                # This is an auxiliar division to read CAN
                html.Div(id='read_can'),

                html.Div([
                    html.Div([
                        html.Label('CACC Control type:',
                            style = {'fontSize': 20},
                        )
                    ], className = 'row'),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Lead', 'value': 'Lead'},
                            {'label': 'Following', 'value': 'Following'}
                        ],
                        value = 'Following',
                        inputStyle = {'width': 15,
                                      'height': 15},
                        labelStyle={'display': 'inline-block'},
                        style = {'fontSize': 20},
                        id = 'car_position'
                    ),
                ], className = 'row', style={'padding': 20}),

                html.Div([
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
                                value = 25,
                                id = 'gap_input',
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                    html.Div([
                        html.Div([
                            html.Label('Target Speed (mph):',
                                style = {'fontSize': 20},
                            )
                        ], className = 'row'),
                        html.Div([
                            dcc.Input(
                                placeholder = 'Enter a target speed...',
                                type = 'number',
                                value = 25,
                                id = 'speed_input',
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                ], className = 'row', style={'padding': 10}),

                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Kp:',
                                style = {'fontSize': 20},
                            )
                        ], className = 'row'),
                        html.Div([
                            dcc.Input(
                                placeholder = 'Prop gain...',
                                type = 'number',
                                value = 0.2,
                                id = 'prop_gain',
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                    html.Div([
                        html.Div([
                            html.Label('Kd:',
                                style = {'fontSize': 20},
                            )
                        ], className = 'row'),
                        html.Div([
                            dcc.Input(
                                placeholder = 'Deriv gain...',
                                type = 'number',
                                value = 0.15,
                                id = 'der_gain',
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                ], className = 'row', style={'padding': 10}),

                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Max accel (mps^2):',
                                style = {'fontSize': 20},
                            )
                        ], className = 'row'),
                        html.Div([
                            dcc.Input(
                                placeholder = 'Max acceleration...',
                                type = 'number',
                                id = 'max_accel',
                                value = 0.9
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                    html.Div([
                        html.Div([
                            html.Label('Min accel (mps^2):',
                                style = {'fontSize': 20},
                            )
                        ], className = 'row'),
                        html.Div([
                            dcc.Input(
                                placeholder = 'Min acceleration...',
                                type = 'number',
                                id = 'min_accel',
                                value = -0.4
                            ),
                        ], className = 'row', style={'padding': 5}),
                    ], className = 'three columns'),
                ], className = 'row', style={'padding': 10}),

            html.Div([
                dcc.Graph(id='live_update_graph'),
            ], className = 'row', style={'padding': 20})


            ])
