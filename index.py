import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import home,maintenance,finance,operation,employees,maintenance_layouts,finance_layouts,operation_layouts

server = app.server
app.layout = html.Div([
    dcc.Location(id='url',pathname='/apps/home', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    elif pathname == "/apps/maintenance":
        return maintenance.layout

    elif pathname == "/apps/operation":
        return operation.layout

    elif pathname == "/apps/finance":
        return finance.layout

    elif pathname == "/apps/employees":
        return employees.layout

    elif pathname == "/apps/maintenance_layouts/available_lch":
        return maintenance_layouts.layout_available_lch
    elif pathname == "/apps/maintenance_layouts/available_ech":
        return maintenance_layouts.layout_available_ech
    elif pathname == "/apps/maintenance_layouts/available_forklifts":
        return maintenance_layouts.layout_available_forklifts
    elif pathname == "/apps/maintenance_layouts/cost_comparison_lch":
        return maintenance_layouts.layout_cost_comparison_lch
    elif pathname == "/apps/maintenance_layouts/cost_comparison_ech":
        return maintenance_layouts.layout_cost_comparison_ech
    elif pathname == "/apps/maintenance_layouts/cost_comparison_forklifts":
        return maintenance_layouts.layout_cost_comparison_forklifts
    elif pathname == "/apps/maintenance_layouts/working_hours_lch":
        return maintenance_layouts.layout_working_hours_lch
    elif pathname == "/apps/maintenance_layouts/working_hours_ech":
        return maintenance_layouts.layout_working_hours_ech
    elif pathname == "/apps/maintenance_layouts/working_hours_forklifts":
        return maintenance_layouts.layout_working_hours_forklifts
    elif pathname == "/apps/maintenance_layouts/availability_vs_repair_cost_ech":
        return maintenance_layouts.layout_availability_vs_repair_cost_ech
    elif pathname == "/apps/maintenance_layouts/availability_vs_repair_cost_lch":
        return maintenance_layouts.layout_availability_vs_repair_cost_lch
    elif pathname == "/apps/maintenance_layouts/availability_vs_repair_cost_forklifts":
        return maintenance_layouts.layout_availability_vs_repair_cost_forklifts

    elif pathname == "/apps/finance_layouts/actual_gp_vs_forecast_layout":
        return finance_layouts.actual_gp_vs_forecast_layout
    elif pathname == "/apps/finance_layouts/maintenance_cost_vs_profit":
        return finance_layouts.maintenance_cost_vs_gp_layout
    elif pathname == "/apps/finance_layouts/profit_margin_variation_layout":
        return finance_layouts.profit_margin_variation_layout
    elif pathname == "/apps/finance_layouts/profit_pie_layout":
        return finance_layouts.profit_pie_layout
    elif pathname == "/apps/finance_layouts/repair_cost_pie_layout":
        return finance_layouts.repair_cost_pie_layout
    elif pathname == "/apps/finance_layouts/fuel_cost_pie_layout":
        return finance_layouts.fuel_cost_pie_layout
    elif pathname == "/apps/finance_layouts/gp_margin_by_machine_layout":
        return finance_layouts.gp_margin_by_machine_layout
    elif pathname == "/apps/finance_layouts/actual_vs_budgeted_repair_cost_layout":
        return finance_layouts.actual_vs_budgeted_repair_cost_layout
    elif pathname == "/apps/finance_layouts/profit_per_box_layout":
        return finance_layouts.profit_per_box_layout
    elif pathname == "/apps/finance_layouts/profit_vs_forecast_layout":
        return finance_layouts.profit_vs_forecast_layout
    elif pathname == "/apps/finance_layouts/budgeted_vs_actual_maintenance_cost_layout":
        return finance_layouts.budgeted_vs_actual_maintenance_cost_layout
    elif pathname == "/apps/finance_layouts/budgeted_vs_actual_fuel_cost_layout":
        return finance_layouts.budgeted_vs_actual_fuel_cost_layout

    elif pathname == "/apps/operation_layouts/lch_hours_vs_boxes_layout":
        return operation_layouts.lch_hours_vs_boxes_layout
    elif pathname == "/apps/operation_layouts/ech_hours_vs_boxes_layout":
        return operation_layouts.ech_hours_vs_boxes_layout
    elif pathname == "/apps/operation_layouts/fork_hours_vs_boxes_layout":
        return operation_layouts.fork_hours_vs_boxes_layout


    else:
        return '404'

if __name__ == '__main__':
     app.run_server(debug=True, port = 8051)