import dash
from dash import dcc
from dash import html
from dash import no_update as nop
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import math
import numpy as np
import os

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Darts score recorder'

def write_darts_to_file(d1, d2, d3):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/darts_record.txt", "a") as f:
        f.write(f"{d1}, {d2}, {d3}\n")

def read_3_dart_avg(avg=True):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/3_dart_avg.txt", "r") as f:
        lines = f.readlines()
    return float(lines[avg].split("= ")[1])

def update_3_dart_avg_file(n_visits, avg):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/3_dart_avg.txt", "w") as f:
        f.write(f"number of visits = {n_visits}\n3 dart average = {avg}")

def convert_score(value):
    if 'D' in value:
        return int(value.split("D")[1]) * 2
    if 'T' in value:
        return int(value.split("T")[1]) * 3
    if value == "Bull":
        return 50
    return int(value)

def update_layout():
    body = dbc.Container([
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.Div(style={"width": "0.5rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-right": "none"}),
            html.Div("Current visit: ", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "2rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div("Darts:", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "1rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div("_____", id="dart_1", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "1rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div("_____", id="dart_2", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "1rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div("_____", id="dart_3", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "3.3rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none"}),
        ]),
        html.Div([
            html.Div(style={"height": "1rem"}),
            html.Div(style={"width": "0.5rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-right": "none"}),
            html.Div("3-dart average: ", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "2rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div("_____", id="3_dart_avg", style={"line-height": "3rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none", "border-right": "none"}),
            html.Div(style={"width": "12.4rem", "margin-bottom": "-1.1rem", "height": "3rem", "display": "inline-block", "border": "0.1rem solid #000", "border-left": "none"}),
        ]),
        html.Div([
            html.Div([
                html.Div([
                    *[html.Button(f"{i}", id=f"btn_{i}") for i in range(1, 6)]
                ]),
                html.Div([
                    *[html.Button(f"{i}", id=f"btn_{i}") for i in range(6, 11)]
                ]),
                html.Div([
                    *[html.Button(f"{i}", id=f"btn_{i}") for i in range(11, 16)]
                ]),
                html.Div([
                    *[html.Button(f"{i}", id=f"btn_{i}") for i in range(16, 21)]                        
                ]),
                html.Div([
                    html.Button("25", id="btn_25"),
                    html.Button("Bull", id="btn_bull"),
                    html.Button("Double", id="btn_double", className="wider_button"),
                    html.Button("Treble", id="btn_treble", className="wider_button")
                ]),
                html.Div([
                    html.Button("⬅", id="btn_backspace", className="backspace_button"),
                    html.Button("Confirm", id="btn_confirm", disabled=True, className="confirm_button")
                ])
            ])
        ]),
    ])
    return body

app.layout = update_layout()

### CALLBACKS
@app.callback(
    *[Output(f"btn_{i}", "children") for i in range(1, 21)],
    Input("btn_1", "children"),
    Input("btn_double", "n_clicks"),
    Input("btn_treble", "n_clicks"),
    prevent_initial_call=True
)
def double_treble_text(btn_1_text, n_double, n_treble):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "double" in trigger:
        if "D" in btn_1_text:
            return [f"{i}" for i in range(1, 21)]
        return [f"D{i}" for i in range(1, 21)]
    if "T" in btn_1_text:
        return [f"{i}" for i in range(1, 21)]
    return [f"T{i}" for i in range(1, 21)]

@app.callback(
    Output("dart_1", "children"),
    Output("dart_2", "children"),
    Output("dart_3", "children"),
    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    Input("btn_25", "n_clicks"),
    Input("btn_bull", "n_clicks"),
    *[State(f"btn_{i}", "children") for i in range(1, 21)],
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_thrown_dart(*args):
    if args[-1] != "_____":
        return nop, nop, nop
    trigger = dash.callback_context.triggered[0]['prop_id']
    btn_names = args[22:-3]

    if 'bull' in trigger:
        if args[-3] == "_____":
            return "Bull", nop, nop
        if args[-2] == "_____":
            return nop, "Bull", nop
        return nop, nop, "Bull"
               
    if '25' in trigger:
        if args[-3] == "_____":
            return "25", nop, nop
        if args[-2] == "_____":
            return nop, "25", nop
        return nop, nop, "Bull"
               
    value = int(trigger.split("btn_")[1].split(".n_clicks")[0])
    
    if args[-3] == "_____":
        return btn_names[value - 1], nop, nop
    if args[-2] == "_____":
        return nop, btn_names[value - 1], nop
    return nop, nop, btn_names[value - 1]
    
@app.callback(
    Output("dart_1", "children", allow_duplicate=True),
    Output("dart_2", "children", allow_duplicate=True),
    Output("dart_3", "children", allow_duplicate=True),
    Input("btn_confirm", "n_clicks"),
    prevent_initial_call=True
)
def record_all_3_darts(n_confirm):
    return "_____", "_____", "_____"

@app.callback(
    Output("btn_confirm", "disabled"),
    Input("dart_3", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3, dart_1, dart_2):
    if dart_3 != "_____":
        write_darts_to_file(dart_1, dart_2, dart_3)
    return dart_3 == "_____"
    
@app.callback(
    Output("3_dart_avg", "children"),
    Input("btn_confirm", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg(n_confirm, dart_1, dart_2, dart_3):
    dart_1 = convert_score(dart_1)
    dart_2 = convert_score(dart_2)
    dart_3 = convert_score(dart_3)

    n_visits = read_3_dart_avg(avg=False)
    current_avg = read_3_dart_avg()
    new_avg = float("%.2f" % (((n_visits * current_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1)))

    update_3_dart_avg_file(n_visits + 1, new_avg)

    return new_avg

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=5000)
