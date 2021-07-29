import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import base64

'''=============================== load data and process data======================================================'''
pd.options.display.float_format = '${:.2f}'.format
df = pd.read_excel('fleet_availability_analysis_aitken.xls')
df['year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
df['month'] = pd.to_datetime(df['date']).dt.strftime('%b')
df[df['machine_type']== 'Laden']

df.columns

'''========================Sort df by year and month=================================================================='''
def get_sums_df(machine_type):
    df1 = df[df['machine_type']== machine_type]
    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    g=df1.groupby(['year','month']).sum()
    g=g.reset_index(level=['year','month'])
    g['month'] = pd.Categorical(g['month'],categories=cats,ordered=True)
    g=g.sort_values(['year','month'])
    g=g.set_index(['year','month'])
    return g

get_sums_df('Laden')
no_of_months = len(get_sums_df('Forklift').index)
'''================================================================================================================='''
years = np.unique(df['year'])
machines = np.unique(df['machine_type'])
'''============================== create options list ============================================================='''
year_options =[{'label':'All','value':'All'}]
for i in years:
    year_options.append({'label': i,'value':i})

machine_opts=[]
for i in machines:
    machine_opts.append({'label': i,'value':i})

'''=======================================Define graphs============================================================='''


def availabile_machines_graph(input1,input2):
    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        # updating the plot
    return go.Scatter(x=df2['date'], y=df2['no_of_available_machines '],
                     name='no_of_available_machines ',
                     line=dict(width=2, color='#660066'))


def machine_working_hours(machine_type):

    g=get_sums_df(machine_type= machine_type)
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=600)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter( y= g['no_of_working_hours'], name='Hours',
                     line=dict(width=2, color='#660066'))
    trace_2 = go.Scatter(y=g['no_of_boxes_handled'], name='Boxes', line=dict(width=2, color='#ff3300'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.update()

    return fig

def profits(machine_type):

    g=get_sums_df(machine_type= machine_type)
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter( y= g['gross_profit'], name='Actual',
                     line=dict(width=2, color='#660066'))
    trace_2 = go.Scatter(y=g['forecasted_profit'], name='Forecast', line=dict(width=2, color='#ff3300'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.update()

    return fig


def boxes_handled(machine_type):

    g=get_sums_df(machine_type= machine_type)
    trace = go.Scatter( y= g['no_of_boxes_handled'],name='no_of_boxes_handled',line=dict(width=2, color='#660066'))
    fig_layout= go.Layout(title='Laden Monthly Containers Handled', hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    figure = go.Figure(data=[trace], layout=fig_layout)
    return figure


def working_hours_hist(input1,input2):

    color_list = ['#003300','#000066','#e60000','#99003d']

    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
        graph_color = color_list[1]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        graph_color = color_list[np.random.randint(0,3)]

    return go.Histogram(x=df2['no_of_working_hours'],
                     name='no_of_working_hours',marker=dict(color=graph_color, line=dict(color='#000000', width=1)),
                     )

def working_hours_scatter(input1):


    df2 = get_sums_df(machine_type=input1)


    return go.Scatter(y=df2['no_of_working_hours'],
                     name='no_of_working_hours_scatter' ,line=dict(width=2, color='#ff0000'))


def availability_graph(input1,input2):
    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        # updating the plot
    availability = df2['no_of_available_machines ']/(df2['no_of_available_machines ']+df2['no_of_break_down_machines '])
    return go.Scatter(x=df2['date'], y=availability,
                     name='no_of_available_machines ',
                     line=dict(width=2, color='#660066'))

def availability_boxplot(input1):

    fig_layout = go.Layout(title='Availability Distribution for All Machines',
                             hovermode='closest', plot_bgcolor='#ffff66', height=250, width=500)
    fig = go.Figure(layout=fig_layout)

    color_list = ['#0000ff','#00ff00','#cc0052']
    machine_list = np.unique(df['machine_type'])

    for i in range(len(machine_list)):

        if input1 == 'All':
            df2 = df[df['machine_type'] == machine_list[i]]
        else:
            df2 = df[(df['year'] == input1) & (df['machine_type'] == machine_list[i])]

            # updating the plot
        df2['availability'] = df2['no_of_available_machines ']/(
                df2['no_of_available_machines ']+df2['no_of_break_down_machines '])
        fig.add_trace(go.Box(y=df2['availability'], x=df2['machine_type'], name=machine_list[i], fillcolor=color_list[i]))

    return fig


def cost_comparison_line(machine_type):
    df2= df[df['machine_type']==machine_type]
    budgeted_cost_cum = df2['budgeted_cost_of_repairs'].cumsum()
    repair_cost_cum = df2['cost_of_repair'].cumsum()

    fig_layout = go.Layout( hovermode='closest', plot_bgcolor='#ffff66', height=250, width=450)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=df2['date'], y=budgeted_cost_cum,
                         name='Budget',
                         line=dict(width=2, color='#660066')))
    fig.add_trace(go.Scatter(x=df2['date'], y=repair_cost_cum,
                             name='Cost',
                             line=dict(width=2, color='#ff0000')))
    fig.update_layout()

    return fig

def hours_vs_boxes_scatter(machine_type):
    df2= df[df['machine_type']==machine_type]
    working_hours = df2['no_of_working_hours']
    boxes_handled = df2['no_of_boxes_handled']

    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=working_hours, y=boxes_handled,  marker=dict(size=5,color='#003300'),
                         name='Budget',mode='markers'))


    fig.update_xaxes(title_text='Working Hours')
    fig.update_yaxes(title_text='Boxes Handled')
    fig.update_layout()

    return fig

def hours_vs_machines_scatter(machine_type):
    df2= df[df['machine_type']==machine_type]
    working_hours = df2['no_of_working_hours']
    available_machines = df2['no_of_available_machines ']

    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=available_machines, y=working_hours,  marker=dict(size=5,color='#003300'),
                         name='Budget',mode='markers'))


    fig.update_xaxes(title_text='Available Machines')
    fig.update_yaxes(title_text='Working Hours')
    fig.update_layout()

    return fig

def cost_pie():
    cost = df.groupby('machine_type').sum()['cost_of_repair']
    machine = df.groupby('machine_type').sum().index
    colors = ['mediumturquoise', '#660066', '#cc0000']

    fig_layout = go.Layout(title='Repair Cost Distribution By Machine Type ',
                           hovermode='closest', plot_bgcolor='#ffff66', height=250, width=500)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Pie(labels=machine, values=cost,
                         name='Budget')),
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    return fig
'''====================================set layouts================================================================='''

fig_1 = machine_working_hours(machine_type='Laden')
fig_1.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Laden').index),
                    )

fig_2 = machine_working_hours(machine_type='ECH')
fig_2.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#80ff80',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('ECH').index),
                    )

fig_3 = machine_working_hours(machine_type='Forklift')
fig_3.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff66',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Monthly Forklift Working Hours and Boxes Handled ')

fig_4 = profits(machine_type='Laden')
fig_4.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Laden').index),
                    title='Monthly Laden Actual Gross Profit vs Forecast ')

fig_5 = profits(machine_type='ECH')
fig_5.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#80ff80',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('ECH').index),
                    title='Monthly ECH Actual Gross Profit vs Forecast ')

fig_6 = profits(machine_type='Forklift')
fig_6.update_layout(autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff66',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Monthly Forklift Actual Gross Profit vs Forecast ')

fig_7 = hours_vs_boxes_scatter(machine_type='Laden')
fig_7.update_layout(title='LCH Working Hours vs Boxes Handled', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2')

fig_8 = hours_vs_boxes_scatter(machine_type='ECH')
fig_8.update_layout(title='ECH Working Hours vs Boxes Handled', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#80ff80')

fig_9 = hours_vs_boxes_scatter(machine_type='Forklift')
fig_9.update_layout(title='Forklift Working Hours vs Boxes Handled', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff66')

fig_10 = hours_vs_machines_scatter(machine_type='Laden')
fig_10.update_layout(title='LCH Availability vs Working Hours', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2')

fig_11 = hours_vs_machines_scatter(machine_type='ECH')
fig_11.update_layout(title='ECH Availability vs Working Hours', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#80ff80')

fig_12 = hours_vs_machines_scatter(machine_type='Forklift')
fig_12.update_layout(title='Forklift Availability vs Working Hours', autosize=True, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff66')
'''================================================================================================================'''
image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'

lch_hours_vs_boxes_layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("MONTHLY LCH WORKING HOURS AND BOXES HANDLED ",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Graph(id='plot1', figure=fig_1, style={'position': 'relative', 'padding-left':
            '10px', 'display': 'inline-block', 'width': '100%', 'height': '100%', 'padding-top': '20px'}),
                  dcc.Link([html.Button('Go Back',
                                        name='test', style={'font-weight': 'bold', 'position': 'absolute', 'width': '75px',
                                                            'left': '10px', 'bottom': '20px', 'height': '25px'})],
                           href='/apps/operation')])

])

ech_hours_vs_boxes_layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("MONTHLY ECH WORKING HOURS AND BOXES HANDLED ",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Graph(id='plot2', figure=fig_2, style={'position': 'relative', 'padding-left':
            '10px', 'display': 'inline-block', 'width': '100%', 'height': '100%', 'padding-top': '20px'}),
                  dcc.Link([html.Button('Go Back',
                                        name='test', style={'font-weight': 'bold', 'position': 'absolute', 'width': '75px',
                                                            'left': '10px', 'bottom': '20px', 'height': '25px'})],
                           href='/apps/operation')])

])

fork_hours_vs_boxes_layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("MONTHLY FORKLIFT WORKING HOURS AND BOXES HANDLED ",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Graph(id='plot3', figure=fig_3, style={'position': 'relative', 'padding-left':
            '10px', 'display': 'inline-block', 'width': '100%', 'height': '100%', 'padding-top': '20px'}),
                  dcc.Link([html.Button('Go Back',
                                        name='test', style={'font-weight': 'bold', 'position': 'absolute', 'width': '75px',
                                                            'left': '10px', 'bottom': '20px', 'height': '25px'})],
                           href='/apps/operation')])

])