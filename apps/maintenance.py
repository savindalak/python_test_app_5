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

def get_averages_df(machine_type):
    df1 = df[df['machine_type']== machine_type]
    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    g=df1.groupby(['year','month']).mean()
    g=g.reset_index(level=['year','month'])
    g['month'] = pd.Categorical(g['month'],categories=cats,ordered=True)
    g=g.sort_values(['year','month'])
    g=g.set_index(['year','month'])
    return g

no_of_months = len(get_sums_df('Forklift').index)
get_averages_df('ECH').columns
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


def average_availabile_machines_graph(machine_type):

    df2 = get_averages_df(machine_type)
        # updating the plot
    return go.Scatter(y=df2['no_of_available_machines '],
                     name='no_of_available_machines ',
                     line=dict(width=2, color='#660066'))


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

    fig_layout = go.Layout( hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=df2['date'], y=budgeted_cost_cum,
                         name='Budget',
                         line=dict(width=2, color='#660066')))
    fig.add_trace(go.Scatter(x=df2['date'], y=repair_cost_cum,
                             name='Cost',
                             line=dict(width=2, color='#ff0000')))
    fig.update_layout()

    return fig


def monthly_repair_cost_vs_availability(machine_type,scale=1000):
    df1= get_averages_df(machine_type=machine_type)
    df2 = get_sums_df(machine_type=machine_type)
    average_availability = df1['availability %']
    repair_cost_cum = df2['cost_of_repair']/scale

    fig_layout = go.Layout( hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(y=average_availability,
                         name='Availability %',
                         line=dict(width=2, color='#660066')))
    fig.add_trace(go.Scatter(y=repair_cost_cum,
                             name='Cost(x $'+'{}'.format(scale)+')',
                             line=dict(width=2, color='#ff0000')))
    fig.update_layout()

    return fig

def hours_vs_boxes_scatter():
    df2= df[df['machine_type']=='Laden']
    working_hours = df2['no_of_working_hours']
    boxes_handled = df2['cost_of_repair']

    fig_layout = go.Layout(title='LCH Working Hours vs Boxes Handled',
                           hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=working_hours, y=boxes_handled,  marker=dict(size=5,color='#003300'),
                         name='Budget',mode='markers'))


    fig.update_xaxes(title_text='Working Hours')
    fig.update_yaxes(title_text='Boxes Handled')
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

trace_1 = average_availabile_machines_graph(machine_type='Laden')

fig_layout_1 = go.Layout(title='Monthly Average of Available LCH Machines',
                   hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
fig_1 = go.Figure(data=[trace_1], layout=fig_layout_1 )
fig_1.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index))



trace_2 = average_availabile_machines_graph(machine_type='ECH')

fig_layout_2 = go.Layout(title='Monthly Average of Available ECH Machines',
                   hovermode='closest', plot_bgcolor='#ffff66', height=250,width =470)
fig_2 = go.Figure(data=[trace_2], layout=fig_layout_2)
fig_2.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index))


trace_3 = average_availabile_machines_graph(machine_type='Forklift')

fig_layout_3 = go.Layout(title='Monthly Average of Available Forklifts',
                   hovermode='closest', plot_bgcolor='#ff66ff', height=250,width =470)
fig_3 = go.Figure(data=[trace_3], layout=fig_layout_3)
fig_3.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index))

fig_4 = cost_comparison_line(machine_type='Laden')
fig_4.update_layout(title='Laden Budget vs Cost Comparison(Cumulative)',plot_bgcolor='#66ffc2', autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4))

fig_5 = cost_comparison_line(machine_type='ECH')
fig_5.update_layout(title='ECH Budget vs Cost Comparison(Cumulative)',autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4))

fig_6 = cost_comparison_line(machine_type='Forklift')
fig_6.update_layout(title='Forklift Budget vs Cost Comparison(Cumulative)',autosize=False,plot_bgcolor='#ff66ff', margin=dict(l=20,r=20,b=30,t=50,pad=4))

trace_7 = working_hours_scatter(input1= 'Laden')
fig_layout_7 = go.Layout(title='Laden Monthly Working Hours',
                   hovermode='closest', plot_bgcolor='#ffff66', height=250,width =470)
fig_7 = go.Figure(data=[trace_7], layout=fig_layout_7)
fig_7.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',
                    xaxis = dict(tickvals =np.arange(40), tickmode = 'array', ticktext=get_sums_df('Laden').index))

trace_8 = working_hours_scatter(input1= 'ECH')
fig_layout_8 = go.Layout(title='ECH Monthly Working Hours',
                   hovermode='closest', plot_bgcolor='#ffff66', height=250,width =470)
fig_8 = go.Figure(data=[trace_8], layout=fig_layout_8)
fig_8.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),
                    xaxis = dict(tickvals =np.arange(40), tickmode = 'array', ticktext=get_sums_df('ECH').index))

trace_9 = working_hours_scatter(input1= 'Forklift')
fig_layout_9 = go.Layout(title='Forklift Monthly Working Hours',
                   hovermode='closest', plot_bgcolor='#ff66ff', height=250,width =470)
fig_9 = go.Figure(data=[trace_9], layout=fig_layout_9)
fig_9.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),
                    xaxis = dict(tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index))

fig_10 = monthly_repair_cost_vs_availability(machine_type='Laden',scale=100)
fig_10.update_layout(title='Laden Monthly Availability vs Monthly Repair Cost',autosize=False,plot_bgcolor='#ff66ff',
                     margin=dict(l=20,r=20,b=30,t=50,pad=4),xaxis = dict(tickvals =np.arange(no_of_months),
                                                                         tickmode = 'array', ticktext=get_sums_df('Forklift').index))

fig_11 = monthly_repair_cost_vs_availability(machine_type='ECH')
fig_11.update_layout(title='ECH Monthly Availability vs Monthly Repair Cost',autosize=False,plot_bgcolor='#ff66ff',
                     margin=dict(l=20,r=20,b=30,t=50,pad=4),xaxis = dict(tickvals =np.arange(no_of_months),
                                                                         tickmode = 'array', ticktext=get_sums_df('Forklift').index))
fig_12 = monthly_repair_cost_vs_availability(machine_type='Forklift',scale=100)
fig_12.update_layout(title='Forklift Monthly Availability vs Monthly Repair Cost',autosize=False,plot_bgcolor='#ff66ff',
                     margin=dict(l=20,r=20,b=30,t=50,pad=4),xaxis = dict(tickvals =np.arange(no_of_months),
                                                                         tickmode = 'array', ticktext=get_sums_df('Forklift').index))

'''================================================================================================================'''
image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'

layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("MAINTENANCE PERFORMANCE",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Link([dcc.Graph(id='plot1', figure=fig_1, style={'position':'absolute','padding-left':
    '10px','height':'200px', 'width':'400px','display': 'inline-block','top':'70px'})],id='link',href='/apps/maintenance_layouts/available_lch'),
            dcc.Link([dcc.Graph(
        id='plot2', figure=fig_2, style={'position':'absolute','left':
    '515px','height':'200px', 'width':'300px','display': 'inline-block','top':'70px'})],href='/apps/maintenance_layouts/available_ech'),
            dcc.Link([dcc.Graph(
        id='plot3', figure=fig_3, style={'position':'absolute','left':
    '1020px','height':'200px', 'width':'400px','display': 'inline-block','top':'70px'})],href='/apps/maintenance_layouts/available_forklifts')],style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot4', figure=fig_4, style={'position':'absolute','top':'340px','padding-left':
    '10px','height':'200px', 'width':'400px','display': 'inline-block'})],id='link',href='/apps/maintenance_layouts/cost_comparison_lch'),
          dcc.Link([dcc.Graph(
              id='plot5', figure=fig_5, style={'position': 'absolute', 'left':
                  '515px', 'top':'340px','height': '200px', 'width': '300px', 'display': 'inline-block'})], href='/apps/maintenance_layouts/cost_comparison_ech'),

        dcc.Link([dcc.Graph(
            id='plot6', figure=fig_6, style={'position': 'absolute','top':'340px','left':
    '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link', href='/apps/maintenance_layouts/cost_comparison_forklifts')],style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot7', figure=fig_7, style={'position':'absolute','top':'610px','padding-left':
        '10px','height':'200px', 'width':'400px','display': 'inline-block'})],id='link',href='/apps/maintenance_layouts/working_hours_lch'),
              dcc.Link([dcc.Graph(
                  id='plot8', figure=fig_8, style={'position': 'absolute', 'left':
                      '515px', 'top':'610px','height': '200px', 'width': '610px', 'display': 'inline-block'})], href='/apps/maintenance_layouts/working_hours_ech'),

            dcc.Link([dcc.Graph(
                id='plot9', figure=fig_9, style={'position': 'absolute','top':'610px','left':
        '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link', href='/apps/maintenance_layouts/working_hours_forklifts')],style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot7', figure=fig_10, style={'position':'absolute','top':'880px','padding-left':
            '10px','height':'200px', 'width':'400px','display': 'inline-block'})],id='link',href='/apps/maintenance_layouts/availability_vs_repair_cost_lch'),
                  dcc.Link([dcc.Graph(
                      id='plot8', figure=fig_11, style={'position': 'absolute', 'left':
                          '515px', 'top':'880px','height': '200px', 'width': '610px', 'display': 'inline-block'})], href='/apps/maintenance_layouts/availability_vs_repair_cost_ech'),

                dcc.Link([dcc.Graph(
                    id='plot9', figure=fig_12, style={'position': 'absolute','top':'880px','left':
            '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link', href='/apps/maintenance_layouts/availability_vs_repair_cost_forklifts')],style={'padding-top':'50px'})

])


