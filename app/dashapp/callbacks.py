from datetime import datetime as dt
import numpy as np
import plotly.express as px
import pandas_datareader as pdr
import pandas as pd
import plotly
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.graph_objs as go
from datetime import datetime, timedelta
import dash_html_components as html
from app.models import *


df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

def register_callbacks(dashapp):
    @dashapp.callback(
        Output(component_id='text-output', component_property='children'),
        [Input('interval-text', 'n_intervals')]
    )
    def update_output_div(n):
        measure = Measure.query.order_by(Measure.id.desc()).first()
        return  [html.Div(id='acel-x', className='mini_container', children=[
            html.H6(np.round(measure.acel_x, 3), id='acel-x_text'),
            html.P('m/s² - Axis X')]),
        html.Div(id='acel-y', className='mini_container', children=[
            html.H6(np.round(measure.acel_y, 3), id='acel-y_text'),
            html.P('m/s² - Axis Y')]),
        html.Div(id='acel-z', className='mini_container', children=[
            html.H6(np.round(measure.acel_z, 3), id='acel-z_text'),
            html.P('m/s² - Axis Z')]),
        html.Div(id='oil', className='mini_container', children=[
            html.H6(np.round(measure.rot_x, 3), id='oil_text'),
            html.P('rad/s - Axis X')]),
        html.Div(id='wells', className='mini_container', children=[
            html.H6(np.round(measure.rot_y, 3), id='well_text'),
            html.P('rad/s - Axis Y')]),
        html.Div(id='gas', className='mini_container', children=[
            html.H6(np.round(measure.rot_z, 3), id='gas_text'),
            html.P('rad/s - Axis Z')]),
        html.Div(id='temp', className='mini_container', children=[
            html.H6(np.round(measure.temperature, 3), id='temp_text'),
            html.P('°C')])]
        
    @dashapp.callback(
        Output('indicator-graphic', 'figure'),
        [Input('yaxis-column', 'value'),
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),        
        Input('year--slider', 'value')])
    def update_graph(yaxis_column_name, xaxis_type, yaxis_type,year_value):
        data = {
            'time': [],
            'temperature': [],
            'acelleration_x': [],
            'acelleration_y': [],
            'acelleration_z': [],
            'rotation_x': [],
            'rotation_y': [],
            'rotation_z': []
        }
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=100)).order_by(Measure.id)
        for measure in measures:
            if yaxis_column_name=='Rotation':
                data['rotation_x'].append(measure.rot_x)
                data['rotation_y'].append(measure.rot_y)
                data['rotation_z'].append(measure.rot_z)
            if yaxis_column_name=='Acelleration':
                data['acelleration_x'].append(measure.acel_x)
                data['acelleration_y'].append(measure.acel_y)
                data['acelleration_z'].append(measure.acel_z)
            if yaxis_column_name=='Temperature':
                data['temperature'].append(measure.temperature)
            data['time'].append(measure.date)
        if yaxis_column_name=='Temperature':
            data = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['temperature']), 
                name='X - Axis', 
                mode= 'lines+markers',
                line_shape='spline'
            ) 
            return {'data': [data], 'layout':{'margin': {'t': 10, 'r': 10, 'b':50}}} 
        if yaxis_column_name=='Acelleration':
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
                name='X - Axis', 
                mode= 'lines+markers',
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acelleration_z']), 
                name='X - Axis', 
                mode= 'lines+markers',
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'margin': {'t': 0, 'b':0, 'r':0,'l':0}}} 
        if yaxis_column_name=='Rotation':
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
                name='X - Axis', 
                mode= 'lines+markers',
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_z']), 
                name='X - Axis', 
                mode= 'lines',
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'margin': {'t': 0, 'b':0, 'r':0,'l':0}}} 

    @dashapp.callback(
        Output('indicator-graphic-online', 'figure'),
        [Input('yaxis-column-online', 'value'),
        Input('xaxis-type-online', 'value'),
        Input('yaxis-type-online', 'value'),        
        Input('interval-online-graphic', 'n_intervals')])
    def update_graph_online(yaxis_column_name, xaxis_type, yaxis_type, n):
        if yaxis_column_name == 'Rotation':
            data = {
                'time': [],
                'rotation_x': [],
                'rotation_y': [],
                'rotation_z': [],
                'std': []
            }
            measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
            for measure in measures:
                data['rotation_x'].append(measure.rot_x)
                data['rotation_y'].append(measure.rot_y)
                data['rotation_z'].append(measure.rot_z)
                data['time'].append(measure.date)
                data['std'].append(0.1)
            df = pd.DataFrame.from_dict(data)
            print(df)
            data1 = [
                go.Scatter(
                    name='Rotation X',
                    x=df['time'],
                    y=df['rotation_x'],
                    mode='lines',
                    line=dict(color='rgb(177, 119, 51)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['rotation_x']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['rotation_x']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(177, 119, 51, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]
            data2 = [
                go.Scatter(
                    name='Rotation Y',
                    x=df['time'],
                    y=df['rotation_y'],
                    mode='lines',
                    line=dict(color='rgb(137, 209, 255)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['rotation_y']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['rotation_y']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(137, 209, 255, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]
            data3 = [
                go.Scatter(
                    name='Rotation Z',
                    x=df['time'],
                    y=df['rotation_z'],
                    mode='lines',
                    line=dict(color='rgb(0, 255, 0)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['rotation_z']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['rotation_z']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(0, 255, 0, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]

            return {'data': data1+data2+data3} 
        if yaxis_column_name == 'Acelleration':
            data = {
                'time': [],
                'acelleration_x': [],
                'acelleration_y': [],
                'acelleration_z': [],
                'std': []
            }
            measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
            for measure in measures:
                data['acelleration_x'].append(measure.acel_x)
                data['acelleration_y'].append(measure.acel_y)
                data['acelleration_z'].append(measure.acel_z)
                data['time'].append(measure.date)
                data['std'].append(0.1)

            df = pd.DataFrame.from_dict(data)
            data1 = [
                go.Scatter(
                    name='Acelleration X',
                    x=df['time'],
                    y=df['acelleration_x'],
                    mode='lines',
                    line=dict(color='rgb(177, 119, 51)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['acelleration_x']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['acelleration_x']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(177, 119, 51, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]
            data2 = [
                go.Scatter(
                    name='Acelleration Y',
                    x=df['time'],
                    y=df['acelleration_y'],
                    mode='lines',
                    line=dict(color='rgb(137, 209, 255)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['acelleration_y']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['acelleration_y']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(137, 209, 255, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]
            data3 = [
                go.Scatter(
                    name='Acelleration Z',
                    x=df['time'],
                    y=df['acelleration_z'],
                    mode='lines',
                    line=dict(color='rgb(0, 255, 0)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['acelleration_z']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['acelleration_z']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(0, 255, 0, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )]
            return {'data': data1+data2+data3} 
        if yaxis_column_name == 'Temperature':    
            data = {
                'time': [],
                'temperature': [],
                'std': []
            }
            measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=10)).order_by(Measure.id)
            for measure in measures:
                data['temperature'].append(measure.temperature)
                data['time'].append(measure.date)
                data['std'].append(0.1)
            df = pd.DataFrame.from_dict(data)
            fig = {'data': [
                go.Scatter(
                    name='Measurement',
                    x=df['time'],
                    y=df['temperature'],
                    mode='lines',
                    line=dict(color='rgb(137, 209, 255)', width=0.75),
                    showlegend=False
                ),
                go.Scatter(
                    name='Upper Bound',
                    x=df['time'],
                    y=df['temperature']+df['std'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=df['time'],
                    y=df['temperature']-df['std'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(137, 209, 255, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )
            ]}           
            fig['layout'] = {'yaxis_title':'Temperature (°C)', 'hovermode': 'x'}
            return fig
