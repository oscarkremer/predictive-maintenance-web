import dash_core_components as dcc
import dash_html_components as html
from app import db
from app.models import *
import pandas as pd
import dash_table
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

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
                    html.H5('Acelleration and Rotation Module', style={'margin-top': '0px'})
                ])
            ]),
            html.Div(className='one-third column', children=[
                    html.Img(id='plotly-image1',src='assets/default.png', style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
            ]), 
        ]),
        html.Div(className='row flex-display', children=[
            html.Div(id='cross-filter-options', className='pretty_container four columns', children=[
                html.H6('Online Graphic', className='control_label'),
                html.P('Filter by well status', className='control_label'),
                dcc.RadioItems(
                    id='xaxis-type-online',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Filter by well status', className='control_label'),
                dcc.RadioItems(
                    id='yaxis-type-online',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Select the Variable:', className='control_label'),
                dcc.Dropdown(
                    id='yaxis-column-online',
                    options=[{'label': i, 'value': i} for i in ['Acelleration', 'Rotation', 'Temperature']],
                    value='Acelleration'
                ),
                html.H6('Database Graphic', className='control_label'),
                html.P('Filter by construction date (or select range in histogram',className='control_label'),
                html.Div(id='well_statuses', className='dash_dropdown'),
                html.P('Filter by well type', className='control_label'),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Filter by well type', className='control_label'),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
                html.P('Filter by well type', className='control_label'),

                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in ['Acelleration', 'Rotation', 'Temperature']],
                    value='Acelleration'
                ),
                html.P('Filter by well type', className='control_label'),
                dcc.Slider(className='rc-slider',
                        id='year--slider',
                        min=1,
                        max=5,
                        value=5,
                        marks={str(year): str(year) for year in range(1,11)},
                        step=None
                ),
                html.H6('Anomalies Statistics', className='control_label'),
                html.Div(className='table', children=[
                    html.Tr(children=[
                        html.Th('Date'),
                        html.Th('Anomaly Type')
                        ]),
                    html.Tr(children=[
                        html.Td('10/31/2020 20:31:21'),
                        html.Td('Frequency'),
                    ]),
                    html.Tr(children=[
                        html.Td('10/31/2020 20:33:21'),
                        html.Td('Outlier'),
                    ]),
                    html.Tr(children=[
                        html.Td('10/31/2020 20:31:21'),
                        html.Td('Frequency'),
                    ]),
                    html.Tr(children=[
                        html.Td('10/31/2020 20:33:21'),
                        html.Td('Outlier'),
                    ]),
                    html.Tr(children=[
                        html.Td('10/31/2020 20:33:21'),
                        html.Td('HTM'),
                    ])
                ]),
            ]),
            html.Div(id='right-column', className='eight columns', children=[
                html.Div(id='text-output', className='row container-display'),
                dcc.Interval(
                    id='interval-text',
                    n_intervals=0
                ),
                html.Div(className='pretty_container',children=[
                    dcc.Graph(id='indicator-graphic-online'),
                    dcc.Interval(
                        id='interval-online-graphic',
                        n_intervals=0
                    )
                ]),
                html.Div(className='pretty_container', children=[
                    dcc.Graph(id='indicator-graphic')
            ])
            ])
        ]),
        html.Div(className='row flex-display', children=[
            html.Div(className='six columns', children=[
                html.Div(className='pretty_container', children=[
                    dcc.Graph(id='anomalies-pie'),
                    dcc.Interval(
                        id='interval-anomalie-graphic',
                        n_intervals=0
                        )                    
                ])
            ]),
            html.Div(className='six columns', children=[
                html.Div(className='pretty_container', children=[
                    dcc.Graph(id='variables-pie'),
                    dcc.Interval(
                        id='interval-pie-graphic',
                        n_intervals=0
                        )
                ])
            ])
        ])
    ])
