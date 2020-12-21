import dash_core_components as dcc
import dash_html_components as html

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
                html.Div(id='gyroscopi-info', className='row container-display', children=[
                    html.Div(id='wells', className='mini_container', children=[
                        html.H6('2921', id='well_text'),
                        html.P('Number of Wells')
                    ]),
                    html.Div(id='gas', className='mini_container', children=[
                        html.H6('2921', id='gas_text'),
                        html.P('Number of gas')
                    ]),
                    html.Div(id='oil', className='mini_container', children=[
                        html.H6('2921', id='oil_text'),
                        html.P('Number of oil')
                    ]),
                    html.Div(id='temp', className='mini_container', children=[
                        html.H6('2921', id='temp_text'),
                        html.P('Number of oil')
                    ]),
                    html.Div(id='acel-x', className='mini_container', children=[
                        html.H6('2921', id='acel-x_text'),
                        html.P('Number of oil')

                    ]),
                    html.Div(id='acel-y', className='mini_container', children=[
                        html.H6('2921', id='acel-y_text'),
                        html.P('Number of oil')

                    ]),
                    html.Div(id='acel-z', className='mini_container', children=[
                        html.H6('2921', id='acel-z_text'),
                        html.P('Number of oil')
                    ])
                ]),
                html.Div(id='countGraphContainer', className='pretty_container', children=[
                    html.Div(id='count_graph1', className='dash-graph', children=[
                        html.Div(className='js-plotly-plot', children=[
                            dcc.Graph(id='example-s',
                                figure={'layout': {
                                        'title': 'Acelleration - metters per second squared',
                                        },
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Axis X'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Axis Y'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Axis Z'}]
                            })])
                    ])
                ]),
                html.Div(id='countGraphContainer2', className='pretty_container', children=[
                    html.Div(id='count_graph2', className='dash-graph', children=[
                        html.Div(className='js-plotly-plot', children=[
                            dcc.Graph(id='example-s2',
                                figure={'layout': {
                                        'title': 'Rotation - radian per second',
                                        },
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[24,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Eixo X'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Eixo Y'},
                                        {'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Eixo Z'}]
                            })])
                    ]),
                ]),
                html.Div(id='countGraphContainer3', className='pretty_container', children=[
                    html.Div(id='count_graph3', className='dash-graph', children=[
                        html.Div(className='js-plotly-plot', children=[
                            dcc.Graph(id='example-s3',
                                figure={
                                    'data': [{'x':[1,2,3,4,5,6,7,8,9,10], 'y':[25,24,24,25,26,24,24,24,25,26], 'type':'line', 'name': 'Temperatura'}]
                            })])
                    ]),
                ])
            ])
        ]),
        html.Div(
            html.Div([
                html.H4('TERRA Satellite Live Feed'),
                html.Div(id='live-update-text'),
                dcc.Graph(id='live-update-graph'),
                dcc.Interval(
                    id='interval-component',
                    interval=1*1000, # in milliseconds
                    n_intervals=0
                )
            ])
            )
    ])
