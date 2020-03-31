import time
import dash
import random
import dash_table
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from collections import deque
from datetime import datetime

def chart_row(id_string):
    return [html.Div(className='one column', children=[
            html.P('1', style={'text-align':'center'})
        ], style={'margin-right':'2.5rem', 'min-width': '50px'}),
        html.Div(className='one column', children=[
            html.P('1', style={'text-align':'center'})
        ], style={'margin-right':'2.5rem', 'min-width': '50px'}),
        html.Div(className='one column', children=[
            html.P('1', style={'text-align':'center'})
        ], style={'margin-right':'2.5rem', 'min-width': '50px'}),
        html.Div(className='seven column', children=[
            dcc.Graph(id=id_string,
            figure={
                'data': [{'x':x_data, 'y':y_data, 'mode':'lines+markers', 'type':'line', 'name': 'Pendulo 2'}],
                'layout': {
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'autosize': 'true',
                    'showlegend':'false',
                    'xaxis': {
                        'showgrid': False, # thin lines in the background
                        'zeroline': False, # thick line at x=0
                        'visible': False,  # numbers below
                    }, # the same for yaxis
                    'yaxis': {
                        'showgrid': False, # thin lines in the background
                        'zeroline': False, # thick line at x=0
                        'visible': False,  # numbers below
                    },
                    'margin': dict(
                    l=0,
                    r=0,
                    b=0,
                    t=0,
                    pad=0
                ),
                }
            }, config={"modeBarButtonsToRemove": ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'zoom3d', 'pan3d', 'resetCameraDefault3d', 'resetCameraLastSave3d', 'hoverClosest3d', 'orbitRotation', 'tableRotation', 'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo', 'toImage', 'sendDataToCloud', 'hoverClosestGl2d', 'hoverClosestPie', 'toggleHover', 'resetViews', 'toggleSpikelines', 'resetViewMapbox']},  style={'width':'100%', 'height':'95%'})
        ], style={'text-align':'center', 'height':'50%', 'width': '55%'}),
        html.Div(className='one column', style={'text-align':'center'}, children=[
            html.P('WORKING', style={'color': 'green'})
        ])]
        
x_data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21, 22, 23]
y_data = [25,24,24,25,26,24,24,24,25,26, 25,24,24,25,26,24,24,24,25,26, 25, 23, 24]
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
df = pd.DataFrame()
df['News'] = ['corona', 'corona-virus', 'coronaaaaaaaa']
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(className='row', children=
        [html.Div(className="twelve columns div-right-panel",
        children=[
            html.Div(className='row div-top-bar',
            children = [
                html.Div(className='two-col', children=[
                    html.Div('Total de Silos', className='p-top-bar'),
                    html.P('20')
                ]),
                html.Div(className='two-col', children=[
                    html.Div('Silos com Grão', className='p-top-bar'),
                    html.P('15')
                ]),
                html.Div(className='two-col', children=[
                    html.Div('Temp. Amb (C)', className='p-top-bar'),
                    html.P('30')
                ]),
                html.Div(className='two-col', children=[
                    html.Div('Umidade Amb', className='p-top-bar'),
                    html.P('70%')
                ]),
                html.Div(className='two-col', children=[
                    html.Div('Margin Level', className='p-top-bar'),
                    html.P('%')
                ]),
                html.Div(className='two-col', children=[
                    html.Div('Open P/L', className='p-top-bar'),
                    html.P('0')
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className='chart-style four columns', children=[ 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-1',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 1'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 2'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 1',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ]),
                html.Div(className='chart-style four columns', children=[ 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-2',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 1'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 2'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 1',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ]),
                html.Div(className='chart-style four columns',children=[
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-3',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pêndulo 3'},
                                            {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pêndulo 5'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 5',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ])
            ]),
                        html.Div(className='row', children=[
                html.Div(className='chart-style four columns', children=[ 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-4',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 1'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 2'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 1',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ]),
                html.Div(className='chart-style four columns', children=[ 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-5',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 1'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 2'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 1',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ]),
                html.Div(className='chart-style four columns',children=[
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-6',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pêndulo 3'},
                                            {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pêndulo 5'}],
                                    'layout': {
                                        'title': 'Temperatura Média Silo 5',
                                        'plot_bgcolor': '#22252b',
                                        'paper_bgcolor': '#22252b',
                                        'yaxis': dict(range=[0, 30])
                                    }
                            })
                        ])
                    ])
                ])
            ]),
            html.Div(className='row div-bottom-panel', children=[
                html.Div(className='display-inlineblock', children=[
                    html.Div(html.Div(className='Select bottom-dropdown has-value is-searchable Select--single', children=[
                            html.Div(className='Select-control', children=[
                                html.Div(className='Select-multi-value-wrapper', children=[
                                    html.Div(className='Select-value', children=[
                                        html.Span('Open Positions (0)', className='Select-value-label')
                                    ]),
                                    html.Div(className='Select-input', style={'display': 'inline-block'})
                                ]),
                                html.Span(className='Select-arrow-zone', children=[
                                    html.Span(className='Select-arrow')
                                ])
                            ], style={'border': "0px solid black"})
                        ])
                    , style={'border': "0px solid black"})
                ]),
                html.Div(className='display-inlineblock float-right', children=[
                    html.Div([
                        html.Div(className='Select bottom-dropdown is-clearable is-searchable Select--single', children=[
                            html.Div(className='Select-control', children=[
                                html.Div(className='Select-multi-value-wrapper', children=[
                                    html.Div('Close order', className='Select-placeholder'),
                                    html.Div(className='Select-input')
                                ]),
                                html.Span(className='Select-arrow-zone', children=[
                                    html.Span(className='Select-arrow')
                                ])
                            ])
                        ])
                    ])
                ]),
                html.Div(className='row table-orders', children=[
                    html.Table(children=[
                        html.Tr(children=[
                            html.Th('Silo'),
                            html.Th('Sensor'),
                            html.Th('Pêndulo'),
                            html.Th('Horário'),
                            html.Th('Temperatura'),
                            html.Th('Média Diário'),
                            html.Th('Média Semanal'),
                            html.Th('Média Mensal'),
                            html.Th('Variação Diária'),
                            html.Th('Variação Semanal'),
                            html.Th('Variação Mensal'),
                            html.Th('Umid-Amb'),
                            html.Th('Temp-Amb')
                        ])
                    ]),
                    html.Div(className='text-center table-orders-empty', children=[
                        html.P('No open positions data row')
                    ])
                ])
            ]),
        ])
        ])])

if __name__ == '__main__':
    app.run_server(debug=True)

               