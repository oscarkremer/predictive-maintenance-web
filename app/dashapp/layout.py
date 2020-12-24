import dash_core_components as dcc
import dash_html_components as html
from app import db
from app.models import *
import pandas as pd
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

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
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='xaxis-type-online',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block'}
                            ),
                            dcc.Dropdown(
                                id='yaxis-column-online',
                                options=[{'label': i, 'value': i} for i in ['Acelleration', 'Rotation', 'Temperature']],
                                value='Acelleration'
                            ),
                            dcc.RadioItems(
                                id='yaxis-type-online',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block'}
                            )
                        ], style={'width': '48%', 'display': 'inline-block'})]),
                    dcc.Graph(id='indicator-graphic-online'),
                    dcc.Interval(
                        id='interval-online-graphic',
                        n_intervals=0
                    ),
                    dcc.Slider(
                        id='year--slider-online',
                        min=1,
                        max=5,
                        value=5,
                        marks={str(year): str(year) for year in range(1,11)},
                        step=None
                    )
                ]),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='xaxis-type',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block'}
                            ),
                            dcc.Dropdown(
                                id='yaxis-column',
                                options=[{'label': i, 'value': i} for i in ['Acelleration', 'Rotation', 'Temperature']],
                                value='Acelleration'
                            ),
                            dcc.RadioItems(
                                id='yaxis-type',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block'}
                            )
                        ], style={'width': '48%', 'display': 'inline-block'})]),
                    dcc.Graph(id='indicator-graphic'),
                    dcc.Slider(
                        id='year--slider',
                        min=1,
                        max=5,
                        value=5,
                        marks={str(year): str(year) for year in range(1,11)},
                        step=None
                    )
            ])
            ])
        ]),
    ])