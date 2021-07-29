import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import base64


image_filename = 'logo.png'# replace with your own image
encoded_icon = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
encoded_reachstacker = base64.b64encode(open('reachstacker.jpg', 'rb').read()).decode('ascii')
encoded_operation = base64.b64encode(open('operation.jpg', 'rb').read()).decode('ascii')
encoded_finance = base64.b64encode(open('finance.jpg', 'rb').read()).decode('ascii')
encoded_employees = base64.b64encode(open('employees.jpeg', 'rb').read()).decode('ascii')

website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'

layout = html.Div([
    html.Div([html.A([html.Img(src='data:image/png;base64,{}'.format(
        encoded_icon),style={'position':'absolute','width':'45px','left':'10px','height':'45px'})],href=website),
        html.H4("PERFORMANCE DASHBOARD",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),



# adding a plot



    html.Div([html.H5('Operation',style={'color':'black','font-weight':'bold'})],style={'position':'absolute','width':'350px','left':'10px','top':'175px',
                                             'height':'50px','background-color':'white','text-align':'center','padding-top':'5px'}),
    dcc.Link([html.Img(title='Operation',src='data:image/png;base64,{}'.format(
                encoded_operation),style={'position':'absolute','width':'350px','left':'10px','top':'200px','padding-top':'15px',
                                             'height':'350px','color':'white'})],href="/apps/operation"),

    html.Div([html.H5('Maintenance',style={'color':'black','font-weight':'bold'})],style={'position':'absolute','width':'350px','left':'390px','top':'175px',
                                             'height':'50px','background-color':'white','text-align':'center','padding-top':'5px'}),
    dcc.Link([html.Img(title='Maintenance', src='data:image/png;base64,{}'.format(
                encoded_reachstacker), style={'position': 'absolute', 'width': '350px', 'left': '390px','top':'200px','padding-top':'15px',
                                              'height': '350px', 'color': 'white'})], href="/apps/maintenance"),

    html.Div([html.H5('Finance',style={'color':'black','font-weight':'bold'})],style={'position':'absolute','width':'350px','left':'780px','top':'175px',
                                             'height':'50px','background-color':'white','text-align':'center','padding-top':'5px'}),
    dcc.Link([html.Img(title='Finance', src='data:image/png;base64,{}'.format(
        encoded_finance), style={'position': 'absolute', 'width': '350px', 'left': '780px','top':'200px', 'padding-top': '15px',
                                      'height': '350px', 'color': 'white'})], href='/apps/finance'),

    html.Div([html.H5('HRM',style={'color':'black','font-weight':'bold'})],style={'position':'absolute','width':'350px','left':'1170px','top':'175px',
                                             'height':'50px','background-color':'white','text-align':'center','padding-top':'5px'}),
    dcc.Link([html.Img(title='Employees', src='data:image/png;base64,{}'.format(
        encoded_employees), style={'position': 'absolute', 'width': '350px', 'left': '1170px','top':'200px', 'padding-top': '15px',
                                 'height': '350px', 'color': 'white'})], href='/apps/employees')

])