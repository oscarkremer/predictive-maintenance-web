from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output


def register_callbacks(dashapp):
    @dashapp.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
    def update_metrics(n):
        lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
        style = {'padding': '5px', 'fontSize': '16px'}
        return [
            html.Span('Longitude: {0:.2f}'.format(lon), style=style),
            html.Span('Latitude: {0:.2f}'.format(lat), style=style),
            html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
        ]


    # Multiple components can update everytime interval gets fired.
    @dashapp.callback(Output('live-update-graph', 'figure'),
                Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        satellite = Orbital('TERRA')
        data = {
            'time': [],
            'Latitude': [],
            'Longitude': [],
            'Altitude': []
        }

        # Collect some data
        for i in range(180):
            time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
            lon, lat, alt = satellite.get_lonlatalt(
                time
            )
            data['Longitude'].append(lon)
            data['Latitude'].append(lat)
            data['Altitude'].append(alt)
            data['time'].append(time)

        # Create the graph with subplots
        fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

        fig.append_trace({
            'x': data['time'],
            'y': data['Altitude'],
            'name': 'Altitude',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
        fig.append_trace({
            'x': data['Longitude'],
            'y': data['Latitude'],
            'text': data['time'],
            'name': 'Longitude vs Latitude',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 2, 1)

        return fig