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

import dash_core_components as dcc

def register_callbacks(dashapp):
    @dashapp.callback(
        Output(component_id='text-output', component_property='children'),
        [Input('yaxis-column-online', 'value'),
        Input('xaxis-type-online', 'value'),
        Input('yaxis-type-online', 'value'),  
        Input('interval-text', 'n_intervals')]
    )
    def update_output_div(yaxis_column_name, xaxis_type, yaxis_type, n):
        measure = Measure.query.order_by(Measure.id.desc()).first()
        minutes = int(xaxis_type.split(' ')[0])
        error_band = yaxis_type
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=minutes)).order_by(Measure.id)
        if yaxis_column_name == 'Rotation':
            data = {
                'time': [],
                'rotation_x': [],
                'rotation_y': [],
                'rotation_z': [],
                'down_rotation_x': [],
                'down_rotation_y': [],
                'down_rotation_z': [],
                'upper_rotation_x': [],
                'upper_rotation_y': [],
                'upper_rotation_z': []
            }
            for measure in measures:
                data['rotation_x'].append(measure.rot_x)
                data['rotation_y'].append(measure.rot_y)
                data['rotation_z'].append(measure.rot_z)
                data['time'].append(measure.date)
                data['down_rotation_x'].append(measure.down_rot_x)
                data['down_rotation_y'].append(measure.down_rot_y)
                data['down_rotation_z'].append(measure.down_rot_z)
                data['upper_rotation_x'].append(measure.upper_rot_x)
                data['upper_rotation_y'].append(measure.upper_rot_y)
                data['upper_rotation_z'].append(measure.upper_rot_z)
            df = pd.DataFrame.from_dict(data)
            data1 = create_data_plot(df, 'rotation_x', error_band, 'Rotation X', 'rgb(177, 119, 51)', 'rgba(177, 119, 51, 0.5)')
            data2 = create_data_plot(df, 'rotation_y', error_band, 'Rotation Y', 'rgb(137, 209, 255)', 'rgba(137, 209, 255, 0.5)')
            data3 = create_data_plot(df, 'rotation_z', error_band, 'Rotation Z', 'rgb(0, 255, 0)', 'rgba(0, 255, 0, 0.5)')
            figure = {'data': data1+data2+data3, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Rotation (rad/s)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name == 'Acceleration':
            data = {
                'time': [],
                'acceleration_x': [],
                'acceleration_y': [],
                'acceleration_z': [],
                'down_acceleration_x': [],
                'down_acceleration_y': [],
                'down_acceleration_z': [],
                'upper_acceleration_x': [],
                'upper_acceleration_y': [],
                'upper_acceleration_z': []
            }
            for measure in measures:
                data['acceleration_x'].append(measure.acel_x)
                data['acceleration_y'].append(measure.acel_y)
                data['acceleration_z'].append(measure.acel_z)
                data['time'].append(measure.date)
                data['down_acceleration_x'].append(measure.down_acel_x)
                data['down_acceleration_y'].append(measure.down_acel_y)
                data['down_acceleration_z'].append(measure.down_acel_z)
                data['upper_acceleration_x'].append(measure.upper_acel_x)
                data['upper_acceleration_y'].append(measure.upper_acel_y)
                data['upper_acceleration_z'].append(measure.upper_acel_z)

            df = pd.DataFrame.from_dict(data)
            data1 = create_data_plot(df, 'acceleration_x', error_band, 'Acceleration X', 'rgb(177, 119, 51)', 'rgba(177, 119, 51, 0.5)' )
            data2 = create_data_plot(df, 'acceleration_y', error_band, 'Acceleration Y', 'rgb(137, 209, 255)', 'rgba(137, 209, 255, 0.5)')
            data3 = create_data_plot(df, 'acceleration_z', error_band, 'Acceleration Z', 'rgb(0, 255, 0)', 'rgba(0, 255, 0, 0.5)')
            figure = {'data': data1+data2+data3, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Acceleration (m/s²)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name == 'Temperature':    
            data = {
                'time': [],
                'temperature': [],
                'down_temperature': [],
                'upper_temperature': []
            }          
            for measure in measures:
                data['temperature'].append(measure.temperature)
                data['down_temperature'].append(measure.down_temperature)
                data['upper_temperature'].append(measure.upper_temperature)
                data['time'].append(measure.date)
            df = pd.DataFrame.from_dict(data)
            data = create_data_plot(df, 'temperature', error_band, 'Temperature', 'rgb(137, 209, 255)', 'rgba(137, 209, 255, 0.5)')
            figure = {'data': data, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Temperature (°C)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        return  [html.Div(className='row container-display', children=[
                    html.Div(id='acel-x', className='mini_container', children=[
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
                    html.P('°C')])
                ]),
                html.Div(className='pretty_container',children=[
                dcc.Graph(
                    id='graphic-online',
                    figure=figure)
                ])]
        
    @dashapp.callback(
        Output('indicator-graphic', 'figure'),
        [Input('yaxis-column', 'value'),
        Input('year-slider', 'value')])
    def update_graph(yaxis_column_name, year_value):
        data = {
            'time': [],
            'temperature': [],
            'acceleration_x': [],
            'acceleration_y': [],
            'acceleration_z': [],
            'rotation_x': [],
            'rotation_y': [],
            'rotation_z': []
        }
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(hours=year_value)).order_by(Measure.id)
        
        for measure in measures:
            if yaxis_column_name=='Rotation':
                data['rotation_x'].append(measure.rot_x)
                data['rotation_y'].append(measure.rot_y)
                data['rotation_z'].append(measure.rot_z)
            if yaxis_column_name=='Acceleration':
                data['acceleration_x'].append(measure.acel_x)
                data['acceleration_y'].append(measure.acel_y)
                data['acceleration_z'].append(measure.acel_z)
            if yaxis_column_name=='Temperature':
                data['temperature'].append(measure.temperature)
            data['time'].append(measure.date)
        if yaxis_column_name=='Temperature':
            data = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['temperature']), 
                name='Temperature', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data], 'layout':{'yaxis': {'height': 350, 'title': {'text': 'Temperature (°C)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name=='Acceleration':
            data1 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acceleration_x']), 
                name='Acceleration X', 
                mode= 'lines',
                line=dict(color='rgb(177, 119, 51)', width=0.75),
                line_shape='spline'
            ) 
            data2 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acceleration_y']), 
                name='Acceleration Y', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acceleration_z']), 
                name='Acceleration Z', 
                mode= 'lines',
                line=dict(color='rgb(0, 255, 0)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Acceleration (m/s²)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name=='Rotation':
            data1 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_x']), 
                name='Rotation X', 
                mode= 'lines',
                line=dict(color='rgb(177, 119, 51)', width=0.75),
                line_shape='spline'
            ) 
            data2 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_y']), 
                name='Rotation Y', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_z']), 
                name='Rotation Z', 
                mode= 'lines',
                line=dict(color='rgb(0, 255, 0)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Rotation (rad/s)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
 
    @dashapp.callback(Output(component_id='anomaly-pie', component_property='children'),
        [Input('interval-anomalie-graphic', 'n_intervals')])
    def update_pie_graph_online(n):
        outlier = Anomaly.query.filter(Anomaly.behavior=='Outlier').count()
        freq = Anomaly.query.filter(Anomaly.behavior=='Frequency').count()
        deep = Anomaly.query.filter(Anomaly.behavior=='DeepAnT').count()
        data = {'variables': ['Outlier', 'Frequency', 'DeepAnT'], 'values': [outlier, freq, deep]}
        df = pd.DataFrame.from_dict(data)
        fig1 = px.pie(df, values='values', names='variables')
        fig1.update_traces(textposition='inside')
        fig1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        acceleration = Anomaly.query.filter(Anomaly.variable=='Acceleration').count()
        rotation = Anomaly.query.filter(Anomaly.variable=='Rotation').count()
        temperature = Anomaly.query.filter(Anomaly.variable=='Temperature').count()
        data = {'variables': ['Acceleration', 'Rotation', 'Temperature'], 'values': [acceleration, rotation, temperature]}
        df = pd.DataFrame.from_dict(data)
        fig2 = px.pie(df, values='values', names='variables')
        fig2.update_traces(textposition='inside')
        fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return [html.Div(className='six columns', children=[
                    html.Div(className='pretty_container', children=[
                        dcc.Graph(figure=fig1)                    
                    ])
                ]),
                html.Div(className='six columns', children=[
                    html.Div(className='pretty_container', children=[
                        dcc.Graph(figure=fig2)
                    ])
                ])]

    @dashapp.callback(Output(component_id='table-anomaly', component_property='children'),
        [Input('interval-anomalie-table', 'n_intervals')])
    def update_pie_graph_online(n):
        table = [html.Tr(children=[
                    html.Th('Date'),
                    html.Th('Anomaly Type'),
                    html.Th('Variable')
                     ])
                ]
        anomalies = Anomaly.query.order_by(Anomaly.id.desc())[:5]
        for anomaly in anomalies:
            table.append(html.Tr(children=[    
                        html.Td(anomaly.date.strftime('%Y-%m-%d %H:%M')),
                        html.Td(anomaly.behavior),
                        html.Td(anomaly.variable),
                    ]))
        return table


def create_data_plot(dataframe, variable, error_band, label, color, band_color):   
    if error_band == 'Actived':
        return [
            go.Scatter(
                name=label,
                x=dataframe['time'],
                y=dataframe[variable],
                mode='lines',
                line=dict(color=color, width=0.75),
                showlegend=False
            ),
            go.Scatter(
                name='Upper Bound',
                x=dataframe['time'],
                y=pd.Series(dataframe['upper_{}'.format(variable)].values),
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Lower Bound',
                x=dataframe['time'],
                y=pd.Series(dataframe['down_{}'.format(variable)].values),
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor=band_color,
                fill='tonexty',
                showlegend=False
            )
        ]
    else:
        return [
            go.Scatter(
                name=label,
                x=dataframe['time'],
                y=dataframe[variable],
                mode='lines',
                line=dict(color=color, width=0.75),
                showlegend=False
            )
        ]
