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
        [html.Div(className="three columns div-left-panel",
        children=[
            html.Div(className='div-info',
            children= [
                html.Div(
                 [html.Img(className='logo', src="/assets/default.png")]
                , style={'text-align': 'center'}),
                html.H6('Garten Automação', className='title-header'),
                html.P('Esta dashboard fornece dados de temperatura, lidos a partir de um sistema de termometria Garten. Os dados são unificados e aplicados a algoritmos inteligentes para detecção e previsão de anomalias.')    
            ]),
            html.Div(className='div-news', children=[
                html.Div([
                    html.Div([
                        html.P('Alarmes', className='p-news'),
                        html.P('Última Atualização : 19:58:35', className='p-news float-right'),
                        html.Div(id='alarms', className='div-bid-ask'),
                        dcc.Interval(id='alarms-interval',
                            interval=5000,
                            n_intervals=0)
                        ])
                ])
            ]),
            html.Div(className='div-currency-toggles',
            children=[
                html.Div(id='bid-ask', className='div-bid-ask'),
                dcc.Interval(id='bid-ask-interval',
                    interval=5000,
                    n_intervals=0)
            ])
        ]),
    html.Div(className="nine columns div-right-panel",
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
                html.Div('Média por Pêndulo', className='section-banner'),
                html.Div(id='metric-div', children=[
                    html.Div(id='metric_header', className='row metric-row', children=[
                        html.Div(className='one column', children=[
                            html.Div('Silo')
                        ], style={'margin-right':'2.5rem', 'min-width': '50px'}),
                        html.Div(className='one column', children=[
                            html.Div('Pêndulo')
                        ], style={'margin-right':'2.5rem', 'min-width': '50px'}),
                        html.Div(className='one column', children=[
                            html.Div('Sensor')
                        ], style={'text-align': 'center'}),
                        html.Div(className='seven columns', children=[
                            html.Div('Temperatura')
                        ], style={'text-align': 'center'}),
                        html.Div(className='one column', children=[
                            html.Div('Estado')
                        ], style={'text-align': 'center'}),
                    ], style={'height':'3rem', 'margin':'1rem 0px', 'text-align':'center'}),
                    html.Div(id='metric-rows', children=[
                        html.Div(className='row metric-row', children=chart_row('pendulo-1'), style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=chart_row('pendulo-2'), style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=[

                        ], style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=[

                        ], style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=[

                        ], style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=[

                        ], style={'height': '8rem', 'width':'100%'}),
                        html.Div(className='row metric-row', children=[

                        ], style={'height': '8rem', 'width':'100%'})
                    ])
                ])
            ]),
            html.Div(className='row', children=[
                html.Div(className='chart-style six columns', children=[
                    html.Div(className='row  chart-top-bar', children=[
                        html.Span('EURUSD ☰ ', className='inline-block chart-title'),
                        html.Div(className='graph-top-right inline-block', children=[
                            html.Div(className='inline-block', children=[
                                html.Div([
                                    html.Div(className='Select dropdown-period has-value is-searchable Select--single', children=[
                                        html.Div(className='Select-control', children=[
                                            html.Div(className='Select-multi-value-wrapper'),
                                            html.Span(className='Select-arrow-zone', children=[
                                                html.Span(className='Select-arrow')
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ]), 
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
                html.Div(className='chart-style six columns',children=[
                    html.Div(className='row  chart-top-bar', children=[
                        html.Span('USDCHF ☰ ', className='inline-block chart-title'),
                        html.Div(className='graph-top-right inline-block', children=[
                            html.Div(className='inline-block', children=[
                                html.Div([
                                    html.Div(className='Select dropdown-period has-value is-searchable Select--single', children=[
                                        html.Div(className='Select-control', children=[
                                            html.Div(className='Select-multi-value-wrapper'),
                                            html.Span(className='Select-arrow-zone', children=[
                                                html.Span(className='Select-arrow')
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ]), 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example',
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


@app.callback(
    dash.dependencies.Output('bid-ask','children'),
    [dash.dependencies.Input('bid-ask-interval', 'n_intervals')]
    )
def update_value(n):
    return  [html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('SILO', className='four-col',style={'color':'white'}),
                        html.P('T(C)', className='four-col', style={'color':'white'}),
                        html.P('10 dias', className='four-col', style={'color':'white'}),      
                        html.P('30 dias', className='four-col', style={'color':'white'}),      
                    ])
                ])
            ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('1', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                        ])
                    ])
                ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('2', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                        ])
                    ])
                ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('7', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                    ])
                ])
            ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('9', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                    ])
                ])
            ]),
                        html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('10', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                        ])
                    ])
                ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('12', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                    ])
                ])
            ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('13', className='four-col'),
                        function_color_text(),
                        function_color_text(),
                        function_color_text()
                    ])
                ])
            ])
            ]


@app.callback(
    dash.dependencies.Output('alarms','children'),
    [dash.dependencies.Input('alarms-interval', 'n_intervals')]
    )
def update_value(n):
    return  [html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('SILO', className='three-col',style={'color':'white'}),
                        html.P('AERA', className='three-col', style={'color':'white'}),
                        html.P('PESTE', className='three-col', style={'color':'white'})      
                    ])
                ])
            ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('1', className='three-col'),
                        alarm_color_text(),
                        alarm_color_text()
                        ])
                    ])
                ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('2', className='three-col'),
                        alarm_color_text(),
                        alarm_color_text()
                        ])
                    ])
                ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('3', className='three-col'),
                        alarm_color_text(),
                        alarm_color_text()
                    ])
                ])
            ]),
            html.Div([
                html.Div(className='row summary', children=[
                    html.Div(className='row', children=[
                        html.P('4', className='three-col'),
                        alarm_color_text(),
                        alarm_color_text()
                    ])
                ])
            ]),
            ]

def function_color_text(botto_lim=25, upp_lim=40):
    value = random.randrange(25,40)
    if value > 75:
        return html.P(value, className='four-col', style={'color': 'red'})
    else:
        if value < 35:
            return html.P(value, className='four-col', style={'color': 'green'})
        else:
            return html.P(value, className='four-col')
        
def alarm_color_text():
    value = random.randrange(10,90)
    if value >= 89:
        return html.P('DANGER', className='three-col', style={'color': 'red'})
    else:
        return html.P('SAFE', className='three-col', style={'color': 'green'})




if __name__ == '__main__':
    app.run_server(debug=True)

               