import dash_core_components as dcc
import dash_html_components as html
from app import db
from app.models import *

layout = html.Div(id='mainContainer', style={'display': "flex", "flex-direction": "column"}, children=
    [
        html.Div(id='output-clientside'),
        html.Div(id='header', className='row flex-display', style={'margin-bottom': '25px'}, children=
        [
            html.Div(className='one-third column', children=[
                html.Img(src='assets/default.png', style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
            ]),
            html.Div(id='title', className='one-half column', children=[
                html.Div([
                    html.H3('Predictive Maintenance Toolkit', style={'margin-bottom': '0px'}),                   
                    html.H5('Acelleration and Rotation Module', style={'margin-top': '0px'})
                ])
            ]),
            html.Div(className='one-third column', children=[
                    html.Img(src='assets/default.png', style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
            ])
        ]),
        html.Div(className='row flex-display', children=[
            html.Div(id='cross-filter-options', className='pretty_container three columns', children=[
                html.P('Filter by construction date (or select range in histogram',className='control_label'),
                html.Div(id='year_slider', className='dcc_control', style={'padding': '0px 25px 25px'}, children=[
                    dcc.Slider(className='rc-slider', children=[
                        html.Div(className='rc-slider-rail'),
                        html.Div(className='rc-slider-track rc-slider-track-1', style={'left': '0\%'}),
                        html.Div(className='rc-slider-step'),
                        html.Div(className='rc-slider-handle rc-slider-handle-1'),
                        html.Div(className='rc-slider-handle rc-slider-handle-2'),
                        html.Div(className='rc-slider-mark')                        
                    ])
                ]),
                html.P('Filter by well status', className='control_label'),
                html.Div(id='well_status_selector', className='dcc_control'),
                html.Div(id='well_statuses', className='dash_dropdown'),
                html.Div(id='lock_selector', className='dcc_control'),
                html.P('Filter by well type', className='control_label'),
                html.Div(id='well_type_selector', className='dcc_control'),
                html.Div(id='well_types', className='dcc_control')
            ]),
            html.Div(id='right-column', className='nine columns', children=[
                html.Div(id='text-output', className='row container-display'),
                dcc.Interval(
                    id='interval-text',
                    n_intervals=0
                ),
                html.Div(
                    html.Div([
                        html.H4('Acelleration Graphs'),
                        dcc.Graph(id='live-acelleration-graph'),
                        dcc.Interval(
                            id='interval-acelleration',
                            n_intervals=0
                        )
                    ])
                ),
                html.Div(
                    html.Div([
                        html.H4('Rotation Graphs'),
                        dcc.Graph(id='live-rotation-graph'),
                        dcc.Interval(
                            id='interval-rotation',
                            n_intervals=0
                        )
                    ])
                ),
                html.Div(
                    html.Div([
                        html.H4('Temperature Graphs'),
                        dcc.Graph(id='live-temperature-graph'),
                        dcc.Interval(
                            id='interval-temperature',
                            n_intervals=0
                        )
                    ])
                )
            ])
        ]),
    ])