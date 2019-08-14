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
    pass
