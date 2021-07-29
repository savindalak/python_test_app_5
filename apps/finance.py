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

def get_sums_df_total():
    df1 = df
    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    g=df1.groupby(['year','month']).sum()
    g=g.reset_index(level=['year','month'])
    g['month'] = pd.Categorical(g['month'],categories=cats,ordered=True)
    g=g.sort_values(['year','month'])
    g=g.set_index(['year','month'])
    return g

get_sums_df('Laden')
get_sums_df_total()
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
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
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

def profits_total():

    g=get_sums_df_total()
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter( y= g['gross_profit'], name='Actual',
                     line=dict(width=2, color='#660066'))
    trace_2 = go.Scatter(y=g['forecasted_profit'], name='Forecast', line=dict(width=2, color='#ff3300'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.update()

    return fig

def profit_margin():

    g=get_sums_df_total()
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    g['gp_margin'] = (g['gross_profit']/g['revenue'])
    trace_1 = go.Scatter( y= g['gp_margin'], name='Actual',
                     line=dict(width=2, color='#660066'))

    fig.add_trace(trace_1)
    fig.update()

    return fig

def profit_margin_by_machine_type():


    fig_layout = go.Layout(hovermode='closest', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    g_ech = get_sums_df('ECH')
    g_ech['gp_margin'] = (g_ech['gross_profit']/g_ech['revenue'])
    trace_1 = go.Scatter( y= g_ech['gp_margin'], name='ECH',
                     line=dict(width=2, color='#ff0000'))

    g_lch = get_sums_df('Laden')
    g_lch['gp_margin'] = (g_lch['gross_profit'] / g_lch['revenue'])
    trace_2 = go.Scatter(y=g_lch['gp_margin'], name='Laden',
                         line=dict(width=2, color='#0033cc'))

    g_fork = get_sums_df('Forklift')
    g_fork['gp_margin'] = (g_fork['gross_profit'] / g_fork['revenue'])
    trace_3 = go.Scatter(y=g_fork['gp_margin'], name='Forklift',
                         line=dict(width=2, color='#40ff00'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.add_trace(trace_3)
    fig.update()

    return fig

def profit_per_box_by_machine_type():


    fig_layout = go.Layout(hovermode='closest', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    g_ech = get_sums_df('ECH')
    g_ech['gp_margin'] = (g_ech['gross_profit']/g_ech['no_of_boxes_handled'])
    trace_1 = go.Scatter( y= g_ech['gp_margin'], name='ECH',
                     line=dict(width=2, color='#ff0000'))

    g_lch = get_sums_df('Laden')
    g_lch['gp_margin'] = (g_lch['gross_profit'] / g_lch['no_of_boxes_handled'])
    trace_2 = go.Scatter(y=g_lch['gp_margin'], name='Laden',
                         line=dict(width=2, color='#0033cc'))

    g_fork = get_sums_df('Forklift')
    g_fork['gp_margin'] = (g_fork['gross_profit'] / g_fork['no_of_boxes_handled'])
    trace_3 = go.Scatter(y=g_fork['gp_margin'], name='Forklift',
                         line=dict(width=2, color='#40ff00'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.add_trace(trace_3)
    fig.update()

    return fig

def maintenance_cost_vs_profit():
    g = get_sums_df_total()
    fig_layout = go.Layout(hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter(y=g['gross_profit'], name='Profit',
                         line=dict(width=2, color='#660066'))
    trace_2 = go.Scatter(y=g['cost_of_repair'], name='Repair cost', line=dict(width=2, color='#ff3300'))

    fig.add_trace(trace_1)
    fig.add_trace(trace_2)
    fig.update()

    return fig

def repair_cost_comparison():

    g=get_sums_df_total()
    fig_layout = go.Layout(hovermode='closest', height=250, width=470)
    fig = go.Figure(layout=fig_layout)
    trace_1 = go.Scatter( y= g['cost_of_repair'], name='Actual',
                     line=dict(width=2, color='#660066'))
    trace_2 = go.Scatter(y=g['budgeted_cost_of_repairs'], name='Budgeted', line=dict(width=2, color='#ff3300'))

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


def cost_comparison_line():
    df2= df
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

def profit_cum_line_graph():
    df2= df
    forecast = df2['forecasted_profit'].cumsum()
    actual = df2['gross_profit'].cumsum()

    fig_layout = go.Layout( hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=df2['date'], y=forecast,
                         name='Forecast',
                         line=dict(width=2, color='#660066')))
    fig.add_trace(go.Scatter(x=df2['date'], y=actual,
                             name='Actual',
                             line=dict(width=2, color='#ff0000')))
    fig.update_layout()

    return fig

def fuel_cost_cum_line_graph():
    df2= df
    forecast = df2['budgeted_cost_of_fuel'].cumsum()
    actual = df2['cost_of_fuel'].cumsum()

    fig_layout = go.Layout( hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Scatter(x=df2['date'], y=forecast,
                         name='Budgeted',
                         line=dict(width=2, color='#660066')))
    fig.add_trace(go.Scatter(x=df2['date'], y=actual,
                             name='Actual',
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

def repair_cost_pie():
    cost = df.groupby('machine_type').sum()['cost_of_repair']
    machine = df.groupby('machine_type').sum().index
    colors = ['mediumturquoise', '#660066', '#cc0000']

    fig_layout = go.Layout(title='Repair Cost Distribution By Machine Type ',
                           hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Pie(labels=machine, values=cost,
                         name='Budget')),
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    return fig

def fuel_cost_pie():
    cost = df.groupby('machine_type').sum()['cost_of_fuel']
    machine = df.groupby('machine_type').sum().index
    colors = ['mediumturquoise', '#660066', '#cc0000']

    fig_layout = go.Layout(title='Fuel Cost Distribution By Machine Type ',
                           hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Pie(labels=machine, values=cost,
                         name='Budget')),
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    return fig

def profit_pie():
    profit = df.groupby('machine_type').sum()['gross_profit']
    machine = df.groupby('machine_type').sum().index
    colors = ['mediumturquoise', '#660066', '#cc0000']

    fig_layout = go.Layout(title='Profit Distribution By Machine Type ',
                           hovermode='closest', plot_bgcolor='#ffff66', height=250, width=470)
    fig = go.Figure(layout=fig_layout)

    fig.add_trace(go.Pie(labels=machine, values=profit,
                         name='Budget')),
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    return fig
'''====================================set layouts================================================================='''

fig_1 = profits_total()
fig_1.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#66ffc2',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Monthly Actual Gross Profit vs Forecast ')

fig_2 = maintenance_cost_vs_profit()
fig_2.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#80ff80',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('ECH').index),
                    title='Monthly Maintenance Cost vs Gross Profit ')

fig_3 = profit_margin()
fig_3.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffff66',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),yaxis=dict(tickformat=".0%"),
                    title='Monthly Profit Margin Variation')

fig_4 = profit_pie()
fig_4.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4))

fig_5 = repair_cost_pie()
fig_5.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4))

fig_6 = fuel_cost_pie()
fig_6.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4))

fig_7 = profit_margin_by_machine_type()
fig_7.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ff99e6',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),yaxis=dict(tickformat=".0%"),
                    title='Monthly GP Margin Comparison By Machine Type')

fig_8 = repair_cost_comparison()
fig_8.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ffb366',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Monthly Actual Repair Cost vs Budgeted Maintenance Cost')

fig_9 = profit_per_box_by_machine_type()
fig_9.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#d6d6c2',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Profit Per Box Handled By Machine Type')

fig_10 = profit_cum_line_graph()
fig_10.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#b3b3ff',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Cumulative Profit vs Forecast')

fig_11 = cost_comparison_line()
fig_11.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#b3ffff',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Cumulative Budgeted Maintenance Cost vs Actual')

fig_12 = fuel_cost_cum_line_graph()
fig_12.update_layout(autosize=False, margin=dict(l=20,r=20,b=30,t=50,pad=4),plot_bgcolor='#ecb3ff',xaxis = dict(
    tickvals =np.arange(no_of_months), tickmode = 'array', ticktext=get_sums_df('Forklift').index),
                    title='Cumulative Budgeted Fuel Cost vs Actual')
'''================================================================================================================'''
image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'

layout = html.Div([
    html.Div([dcc.Link([html.Img(src='data:image/png;base64,{}'.format(
        encoded_image),style={'position':'absolute','left':'10px','width':'45px','height':'45px'})],href='/apps/home'),
        html.H5("FINANCIAL PERFORMANCE",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),


# adding a plot

    html.Div([dcc.Link([dcc.Graph(id='plot1', figure=fig_1, style={'position':'absolute','padding-left':
    '10px','height':'200px', 'width':'400px','display': 'inline-block','top':'70px'})],id='link',href='/apps/finance_layouts/actual_gp_vs_forecast_layout'),
            dcc.Link([dcc.Graph(
        id='plot2', figure=fig_2, style={'position':'absolute','left':
    '515px','height':'200px', 'width':'300px','display': 'inline-block','top':'70px'})],href='/apps/finance_layouts/maintenance_cost_vs_profit'),
            dcc.Link([dcc.Graph(
        id='plot3', figure=fig_3, style={'position':'absolute','left':
    '1020px','height':'200px', 'width':'400px','display': 'inline-block','top':'70px'})],href='/apps/finance_layouts/profit_margin_variation_layout')],style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot4', figure=fig_4, style={'position':'absolute','top':'340px','padding-left':
    '10px','height':'200px', 'width':'400px','display': 'inline-block'})],id='link',href='/apps/finance_layouts/profit_pie_layout'),
          dcc.Link([dcc.Graph(
              id='plot5', figure=fig_5, style={'position': 'absolute', 'left':
                  '515px', 'top':'340px','height': '200px', 'width': '300px', 'display': 'inline-block'})], href='/apps/finance_layouts/repair_cost_pie_layout'),

        dcc.Link([dcc.Graph(
            id='plot6', figure=fig_6, style={'position': 'absolute','top':'340px','left':
    '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link', href='/apps/finance_layouts/fuel_cost_pie_layout')],style={'padding-top':'50px'}),

    html.Div([dcc.Link([dcc.Graph(id='plot7', figure=fig_7, style={'position':'absolute','top':'610px','padding-left':
        '10px','height':'200px', 'width':'400px','display': 'inline-block'})],id='link',href='/apps/finance_layouts/gp_margin_by_machine_layout'),
              dcc.Link([dcc.Graph(
                  id='plot8', figure=fig_8, style={'position': 'absolute', 'left':
                      '515px', 'top':'610px','height': '200px', 'width': '300px', 'display': 'inline-block'})], href='/apps/finance_layouts/actual_vs_budgeted_repair_cost_layout'),

            dcc.Link([dcc.Graph(
                id='plot9', figure=fig_9, style={'position': 'absolute','top':'610px','left':
        '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link', href='/apps/finance_layouts/profit_per_box_layout')],style={'padding-top':'50px'}),

    html.Div(
        [dcc.Link([dcc.Graph(id='plot10', figure=fig_10, style={'position': 'absolute', 'top': '880px', 'padding-left':
            '10px', 'height': '200px', 'width': '400px', 'display': 'inline-block'})], id='link', href='/apps/finance_layouts/profit_vs_forecast_layout'),
         dcc.Link([dcc.Graph(
             id='plot11', figure=fig_11, style={'position': 'absolute', 'left':
                 '515px', 'top': '880px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})],
             href='/apps/finance_layouts/budgeted_vs_actual_maintenance_cost_layout'),

         dcc.Link([dcc.Graph(
             id='plot12', figure=fig_12, style={'position': 'absolute', 'top': '880px', 'left':
                 '1020px', 'height': '200px', 'width': '300px', 'display': 'inline-block'})], id='link',
             href='/apps/finance_layouts/budgeted_vs_actual_fuel_cost_layout')], style={'padding-top': '50px'})

])


