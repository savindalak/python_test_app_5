import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import base64

'''=============================== load data and process data======================================================'''
pd.options.display.float_format = '${:.2f}'.format
df = pd.read_excel('fleet_availability_analysis_aitken.xls',sheet_name='employees')
df.columns
'''================================================================================================================'''


def employee_attendance():

    g=df
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=330, width=740)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter(x=g['month'], y= g['attendance(%)'], name='Attendance',
                     line=dict(width=2, color='#660066'))
    fig.add_trace(trace_1)
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Employee Attendance')
    fig.update()

    return fig

def employee_turnover():

    g=df
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=330, width=740)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter(x=g['month'], y= g['turnover'], name='Turnover',
                     line=dict(width=2, color='#660066'))
    fig.add_trace(trace_1)
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Employee Turnover')
    fig.update()

    return fig

def employee_training_hours():

    g=df
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=330, width=740)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter(x=g['month'], y= g['training hours'], name='Training',
                     line=dict(width=2, color='#660066'))
    fig.add_trace(trace_1)
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Employee Training Hours')
    fig.update()

    return fig

def attendance_vs_turnover_scatter():
    df2= df
    attendance = df2['attendance(%)']
    turnover = df2['turnover']

    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=330, width=740)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=attendance, y=turnover,  marker=dict(size=5,color='#003300'),
                         name='attendance_vs_turnover',mode='markers'))


    fig.update_xaxes(title_text='Attendance')
    fig.update_yaxes(title_text='Employee Turnover')
    fig.update_layout()

    return fig

'''====================================set layouts================================================================='''

fig_1 = employee_attendance()
fig_1.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',
                    title='Monthly employee attendance level - 2019')

fig_2 = employee_turnover()
fig_2.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#79ff4d',
                    title='Monthly employee turnover - 2019')

fig_3 = employee_training_hours()
fig_3.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ff66ff',
                    title='Monthly training hours - 2019')

fig_4 = attendance_vs_turnover_scatter()
fig_4.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff4d',
                    title='Employee Turnover vs Attendance')

'''================================================================================================================'''
image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("EMPLOYEES",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Link([dcc.Graph(id='plot1', figure=fig_1, style={'position':'absolute','padding-left':
    '10px','display': 'inline-block','top':'70px'})],id='link',href='/apps/app5/1'),
              dcc.Link([dcc.Graph(id='plot2', figure=fig_2, style={'position':'absolute','padding-left':
    '770px','display': 'inline-block','top':'70px'})],id='link',href='/apps/app5/1'),
              ],
             style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot3', figure=fig_3, style={'position': 'absolute', 'padding-left':
                  '10px', 'display': 'inline-block', 'top': '420px'})], id='link', href='/apps/app5/1'),
            dcc.Link([dcc.Graph(id='plot2', figure=fig_4, style={'position':'absolute','padding-left':
    '770px','display': 'inline-block','top':'420px'})],id='link',href='/apps/app5/1'),
              ],
             style={'padding-top': '50px'}),

   ])