import dash_core_components as dcc
import dash_html_components as html
from app import db
from app.models import *
import pandas as pd
import dash_table

URL_WEB = 'http://104.154.161.53:5000'

layout = html.Div(id='mainContainer', style={'display': "flex", "flex-direction": "column"}, children=
    [
        html.Div(id='output-clientside'),
        html.Div(id='header', className='row flex-display', style={'margin-bottom': '25px'}, children=
        [
            html.Div(className='one-third column', children=[
                html.Img(id='plotly-image',src='assets/default.png', style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
            ]),
            html.Div(id='title', className='one-half column', children=[
                html.Div([
                    html.H3('Predictive Maintenance Toolkit', style={'margin-bottom': '0px'}),                   
                    html.H5('Acceleration and Rotation Module', style={'margin-top': '0px'})
                ])
            ]),
            html.Div(className='one-third column', children=[
                html.Div(children=[
                html.A(
                    html.Button('Logout', id='learn-more-button'),
                    href='{}/logout'.format(URL_WEB)),

                html.A(
                    html.Button('Account', id='account-button'),
                    href='{}/account'.format(URL_WEB))
                ])
            ]), 
        ]),
        html.Div(className='row flex-display', children=[
            html.Div(id='cross-filter-options', className='pretty_container three columns', children=[
                html.H6('Online Graphic', className='control_label'),
                html.P('Select readings in the last', className='control_label'),
                dcc.RadioItems(
                    id='xaxis-type-online',
                    options=[{'label': i, 'value': i} for i in ['10 minutes', '30 minutes', '60 minutes']],
                    value='10 minutes',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Error Band', className='control_label'),
                dcc.RadioItems(
                    id='yaxis-type-online',
                    options=[{'label': i, 'value': i} for i in ['Actived', 'Deactived']],
                    value='Actived',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Select the Variable:', className='control_label'),
                dcc.Dropdown(
                    id='yaxis-column-online',
                    options=[{'label': i, 'value': i} for i in ['Acceleration', 'Rotation', 'Temperature']],
                    value='Acceleration'
                ),
                html.H6('Database Graphic', className='control_label'),
                html.P('Select the variable', className='control_label'),
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in ['Acceleration', 'Rotation', 'Temperature']],
                    value='Acceleration'
                ),
                html.P('Show the points of the last (hours)', className='control_label'),
                dcc.Slider(className='rc-slider',
                        id='year-slider',
                        min=1,
                        max=10,
                        value=2,
                        marks={str(year): str(year) for year in range(1,11)},
                        step=None
                ),
                html.H6('Anomalies Statistics', className='control_label'),
                html.Div(className='table', id='table-anomaly', style={"overflow":"auto"} ),
                dcc.Interval(
                    id='interval-anomalie-table',
                    n_intervals=0,
                    interval=60000
                )
            ]),
            html.Div(id='right-column', className='nine columns', children=[
                html.Div(id='text-output'),
                dcc.Interval(
                    id='interval-text',
                    n_intervals=0,
                    interval=20000
                ),
                html.Div(className='pretty_container', children=[
                    dcc.Graph(id='indicator-graphic')
            ])
            ])
        ]),
        html.Div(className='row flex-display', id='anomaly-pie'),
        dcc.Interval(
            id='interval-anomalie-graphic',
            n_intervals=0,
            interval=60000
        ) 
    ])
