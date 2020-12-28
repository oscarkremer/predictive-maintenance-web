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
                name='Temperature', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data], 'layout':{'yaxis': {'height': 350, 'title': {'text': 'Temperature (°C)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name=='Acelleration':
            data1 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acelleration_x']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(177, 119, 51)', width=0.75),
                line_shape='spline'
            ) 
            data2 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acelleration_y']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['acelleration_z']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(0, 255, 0)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Acelleration (m/s²)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name=='Rotation':
            data1 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_x']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(177, 119, 51)', width=0.75),
                line_shape='spline'
            ) 
            data2 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_y']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                line_shape='spline'
            ) 
            data3 = plotly.graph_objs.Scatter( 
                x=list(data['time']), 
                y=list(data['rotation_z']), 
                name='X - Axis', 
                mode= 'lines',
                line=dict(color='rgb(0, 255, 0)', width=0.75),
                line_shape='spline'
            ) 
            return {'data': [data1,data2,data3], 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Rotation (rad/s)'}},'margin': {'t':10, 'r':10, 'b':50}}} 

    @dashapp.callback(
        Output('indicator-graphic-online', 'figure'),
        [Input('yaxis-column-online', 'value'),
        Input('xaxis-type-online', 'value'),
        Input('yaxis-type-online', 'value'),        
        Input('interval-online-graphic', 'n_intervals')])
    def update_graph_online(yaxis_column_name, xaxis_type, yaxis_type, n):
        minutes = int(xaxis_type.split(' ')[0])
        error_band = yaxis_type
        measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=minutes)).order_by(Measure.id)
        if yaxis_column_name == 'Rotation':
            data = {
                'time': [],
                'rotation_x': [],
                'rotation_y': [],
                'rotation_z': [],
                'std': []
            }
            for measure in measures:
                data['rotation_x'].append(measure.rot_x)
                data['rotation_y'].append(measure.rot_y)
                data['rotation_z'].append(measure.rot_z)
                data['time'].append(measure.date)
                data['std'].append(0.1)
            df = pd.DataFrame.from_dict(data)
            data1 = create_data_plot(df, 'rotation_x', error_band)
            data2 = create_data_plot(df, 'rotation_y', error_band)
            data3 = create_data_plot(df, 'rotation_z', error_band)
            return {'data': data1+data2+data3, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Rotation (rad/s)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name == 'Acelleration':
            data = {
                'time': [],
                'acelleration_x': [],
                'acelleration_y': [],
                'acelleration_z': [],
                'std': []
            }
            for measure in measures:
                data['acelleration_x'].append(measure.acel_x)
                data['acelleration_y'].append(measure.acel_y)
                data['acelleration_z'].append(measure.acel_z)
                data['time'].append(measure.date)
                data['std'].append(0.1)

            df = pd.DataFrame.from_dict(data)
            data1 = create_data_plot(df, 'acelleration_x', error_band)
            data2 = create_data_plot(df, 'acelleration_y', error_band)
            data3 = create_data_plot(df, 'acelleration_z', error_band)
            return {'data': data1+data2+data3, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Acelleration (m/s²)'}},'margin': {'t':10, 'r':10, 'b':50}}} 
        if yaxis_column_name == 'Temperature':    
            data = {
                'time': [],
                'temperature': [],
                'std': []
            }
            for measure in measures:
                data['temperature'].append(measure.temperature)
                data['time'].append(measure.date)
                data['std'].append(0.1)
            df = pd.DataFrame.from_dict(data)
            data = create_data_plot(df, 'temperature', error_band)
            return {'data': data, 'layout':{'height': 350, 'yaxis': {'title': {'text': 'Temperature (°C)'}},'margin': {'t':10, 'r':10, 'b':50}}} 


    @dashapp.callback(Output('variables-pie', 'figure'),
        [Input('interval-pie-graphic', 'n_intervals')])
    def update_pie_graph_online(n):
        df = px.data.gapminder().query("continent == 'Asia'")
        fig = px.pie(df, values='pop', names='country')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return fig

    @dashapp.callback(Output('anomalies-pie', 'figure'),
        [Input('interval-anomalie-graphic', 'n_intervals')])
    def update_pie_graph_online(n):
        data = {'variables': ['acelleration', 'rotation', 'temperature'], 'values': [10, 12, 2]}
        df = pd.DataFrame.from_dict(data)
        fig = px.pie(df, values='values', names='variables')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return fig

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
                y=dataframe[variable]+dataframe['std'],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Lower Bound',
                x=dataframe['time'],
                y=dataframe[variable]-dataframe['std'],
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
                name='Measurement',
                x=dataframe['time'],
                y=dataframe[variable],
                mode='lines',
                line=dict(color='rgb(137, 209, 255)', width=0.75),
                showlegend=False
            )
        ]