
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
                html.Div(className='chart-style twelve columns', children=[ 
                    html.Div([
                        html.Div(className='chart-graph js-plotly-plot', children=[
                            dcc.Graph(id='example-s',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 1'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Pendulo 2'}],
                                    'layout': {
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