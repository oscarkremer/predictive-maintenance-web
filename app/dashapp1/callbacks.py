from datetime import datetime as dt
import numpy as np
import pandas_datareader as pdr
import plotly
from dash.dependencies import Input
from dash.dependencies import Output
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
import dash_html_components as html
from app.models import *

def register_callbacks(dashapp):
    @dashapp.callback(Output('live-acelleration-graph', 'figure'),
                [Input('interval-acelleration', 'n_intervals')])
    def update_acelleration_live(n):
        data = {
            'time': [],
            'acelleration_x': [],
            'acelleration_y': [],
            'acelleration_z': []
        }
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
        for measure in measures:
            data['acelleration_x'].append(measure.acel_x)
            data['acelleration_y'].append(measure.acel_y)
            data['acelleration_z'].append(measure.acel_z)
            data['time'].append(measure.date)
        data1 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['acelleration_x']), 
            name='X - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        )
        data2 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['acelleration_y']), 
            name='Y - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        )
        data3 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['acelleration_z']), 
            name=' Z - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        ) 
        return {'data': [data1, data2, data3]} 
    @dashapp.callback(Output('live-rotation-graph', 'figure'),
        [Input('interval-rotation', 'n_intervals')])
    def update_rotation_live(n):
        data = {
            'time': [],
            'rotation_x': [],
            'rotation_y': [],
            'rotation_z': []
        }
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
        for measure in measures:
            data['rotation_x'].append(measure.rot_x)
            data['rotation_y'].append(measure.rot_y)
            data['rotation_z'].append(measure.rot_z)
            data['time'].append(measure.date)
        data1 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['rotation_x']), 
            name='X - Axis', 
            mode= 'lines+markers',
            line_shape='spline'

        ) 
        data2 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['rotation_y']), 
            name='Y - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        ) 
        data3 = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['rotation_z']), 
            name=' Z - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        ) 
        return {'data': [data1, data2, data3]} 
    @dashapp.callback(Output('live-temperature-graph', 'figure'),
        [Input('interval-temperature', 'n_intervals')])
    def update_temperature_live(n):
        data = {
            'time': [],
            'temperature': []
        }
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
        for measure in measures:
            data['temperature'].append(measure.temperature)
            data['time'].append(measure.date)
        data = plotly.graph_objs.Scatter( 
            x=list(data['time']), 
            y=list(data['temperature']), 
            name='X - Axis', 
            mode= 'lines+markers',
            line_shape='spline'
        ) 
        return {'data': [data]} 
    @dashapp.callback(
        Output(component_id='text-output', component_property='children'),
        [Input('interval-text', 'n_intervals')]
    )
    def update_output_div(n):
        measure = Measure.query.order_by(Measure.id.desc()).first()
        print(measure.acel_x)
        return  [html.Div(id='acel-x', className='mini_container', children=[
            html.H6(np.round(measure.acel_x, 3), id='well_text'),
            html.P('m/s² - Axis X')]),
        html.Div(id='acel-y', className='mini_container', children=[
            html.H6(np.round(measure.acel_y, 3), id='gas_text'),
            html.P('m/s² - Axis Y')]),
        html.Div(id='acel-z', className='mini_container', children=[
            html.H6(np.round(measure.acel_z, 3), id='oil_text'),
            html.P('m/s² - Axis Z')]),
        html.Div(id='temp', className='mini_container', children=[
            html.H6(np.round(measure.rot_x, 3), id='temp_text'),
            html.P('m/s² - Axis X')]),
        html.Div(id='wells', className='mini_container', children=[
            html.H6(np.round(measure.rot_y, 3), id='acel-x_text'),
            html.P('Number of oil')]),
        html.Div(id='gas', className='mini_container', children=[
            html.H6(np.round(measure.rot_z, 3), id='acel-y_text'),
            html.P('Number of oil')]),
        html.Div(id='oil', className='mini_container', children=[
            html.H6(np.round(measure.temperature, 3), id='acel-z_text'),
            html.P('Number of oil')])]
        