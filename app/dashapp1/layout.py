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
                    html.H3('New York Oil and Gas', style={'margin-bottom': '0px'}),                   
                    html.H5('Acelleration and Rotation', style={'margin-top': '0px'})
                ])
            ]),
            html.Div(className='one-third column', children=[
                    html.Img(src='assets/default.png', style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
            ])
        ]),
        html.Div(className='row flex-display'),
        html.Div(className='row flex-display'),
        html.Div(className='row flex-display'),
        html.Div(className='row flex-display')
    ])