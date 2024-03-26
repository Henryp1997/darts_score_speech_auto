import dash
from dash import html
from dash import no_update as nop
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import math
import os
import pandas as pd
from datetime import datetime

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Darts score recorder'

def write_darts_to_file(d1, d2, d3):
    csv_file = f"{os.path.dirname(os.path.realpath(__file__))}/darts_record.csv"
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    darts = [d1, d2, d3]
    if 'Bull' in darts:
        darts[darts.index('Bull')] = 50

    total = sum([int(i) for i in [convert_score(d1), convert_score(d2), convert_score(d3)]])

    with open(csv_file, "a") as f:
        f.write(f"\n{now}, {darts[0]}, {darts[1]}, {darts[2]}, {total}")

def read_3_dart_avg(avg=True):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/3_dart_avg.txt", "r") as f:
        lines = f.readlines()
    return float(lines[avg].split("= ")[1])

def update_3_dart_avg_file(n_visits, avg):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/3_dart_avg.txt", "w") as f:
        f.write(f"number of visits = {n_visits}\n3 dart average = {avg}")

def record_miss_bull_25(name, d1, d2):
    # what value to show in the top score bar
    val_dict = {"miss": "0", "bull": "Bull", "25": "25"}
    if d1 == "_____":
        return val_dict[name], nop, nop
    if d2 == "_____":
        return nop, val_dict[name], nop
    return nop, nop, val_dict[name]

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
        html.Div(id="hidden_div1", style={"display": "none"}),
        html.Div("0", id="n_visits", style={"display": "none"}),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.Div(style={"height": "0.5rem"}),
            html.Div("..", style={"color": "black", "display": "inline-block"}),
            html.Div("Darts:", style={"color": "white", "display": "inline-block"}),
            html.Div("......", style={"color": "black", "display": "inline-block"}),
            html.Div("_____", id="dart_1", style={"color": "white", "display": "inline-block"}),
            html.Div("......", style={"color": "black", "display": "inline-block"}),
            html.Div("_____", id="dart_2", style={"color": "white", "display": "inline-block"}),
            html.Div("......", style={"color": "black", "display": "inline-block"}),
            html.Div("_____", id="dart_3", style={"color": "white", "display": "inline-block"}),
            html.Div(style={"height": "0.5rem"}),
        ], style={"border": "2px solid #fff"}),
        html.Div(style={"height": "0.5rem"}),
        html.Div([
            html.Div(style={"height": "0.5rem"}),
            html.Div("..", style={"color": "black", "display": "inline-block"}),
            html.Div("3-dart average (current session):", style={"color": "white", "display": "inline-block"}),
            html.Div("......", style={"color": "black", "display": "inline-block"}),
            html.Div("_____", id="3_dart_avg_current", style={"color": "white", "display": "inline-block"}),
            html.Div(style={"height": "0.5rem"}),
        ], style={"border": "2px solid #fff"}),
        html.Div(style={"height": "0.5rem"}),
        html.Div([
            html.Div(style={"height": "0.5rem"}),
            html.Div("..", style={"color": "black", "display": "inline-block"}),
            html.Div("3-dart average (all time):", style={"color": "white", "display": "inline-block"}),
            html.Div("......", style={"color": "black", "display": "inline-block"}),
            html.Div("_____", id="3_dart_avg", style={"color": "white", "display": "inline-block"}),
            html.Div(style={"height": "0.5rem"}),
        ], style={"border": "2px solid #fff"}),
        html.Div(style={"height": "0.5rem"}),
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
                    html.Button("Miss", id="btn_miss"),
                ]),
                html.Div([
                    html.Button("Double", id="btn_double", className="green_button", style={"width": "6.9rem"}),
                    html.Button("Treble", id="btn_treble", className="green_button", style={"width": "6.9rem"}),
                    html.Button("⬅", id="btn_backspace", className="backspace_button"),
                    html.Button("\u2714", id="btn_confirm", disabled=True, className="green_button")
                ])
            ])
        ]),
    ])
    return body

app.layout = update_layout()

### CALLBACKS
@app.callback(
    Output("3_dart_avg", "children"),
    Input("btn_1", "n_clicks")
)
def init_avg_file(n):
    # use btn1 as an input but only trigger this callback once - on page load
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == ".":
        df = pd.read_csv(f"{os.path.dirname(os.path.realpath(__file__))}/darts_record.csv")
        n_visits = len(df)
        avg = float("%.2f" % df['Total'].mean())
        if math.isnan(avg):
            avg = "0"
        update_3_dart_avg_file(n_visits, avg)
        return str(avg)
    return nop

@app.callback(
    *[Output(f"btn_{i}", "children") for i in range(1, 21)],
    Input("btn_1", "children"),
    Input("btn_double", "n_clicks"),
    Input("btn_treble", "n_clicks"),
    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    prevent_initial_call=True
)
def double_treble_text(btn_1_text, n_double, n_treble, *btns):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "double" in trigger:
        if "D" in btn_1_text:
            return [f"{i}" for i in range(1, 21)]
        return [f"D{i}" for i in range(1, 21)]
    elif "treble" in trigger:
        if "T" in btn_1_text:
            return [f"{i}" for i in range(1, 21)]
        return [f"T{i}" for i in range(1, 21)]
      
    # below code executed if one of the number buttons triggered this callback
    # just returns the button texts to non double or treble after each input
    return [f"{i}" for i in range(1, 21)]

@app.callback(
    Output("dart_1", "children"),
    Output("dart_2", "children"),
    Output("dart_3", "children"),
    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    Input("btn_25", "n_clicks"),
    Input("btn_bull", "n_clicks"),
    Input("btn_miss", "n_clicks"),
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
    btn_names = args[23:-3]
    
    value = trigger.split("btn_")[1].split(".n_clicks")[0]
    if value in ['miss', 'bull', '25']:
        return record_miss_bull_25(value, args[-3], args[-2])            
    
    value = int(value)
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
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_all_3_darts(n_confirm, d1, d2, d3):
    write_darts_to_file(d1, d2, d3)
    return "_____", "_____", "_____"

@app.callback(
    Output("dart_1", "children", allow_duplicate=True),
    Output("dart_2", "children", allow_duplicate=True),
    Output("dart_3", "children", allow_duplicate=True),
    Input("btn_backspace", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def delete_dart_input(n_backspace, d1, d2, d3):
    if d3 != "_____":
        return nop, nop, "_____"
    if d2 != "_____":
        return nop, "_____", "_____"
    return "_____", "_____", "_____"

@app.callback(
    Output("btn_confirm", "disabled"),
    Input("dart_3", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3, dart_1, dart_2):
    return dart_3 == "_____"
    
@app.callback(
    Output("3_dart_avg_current", "children"),
    Output("n_visits", "children"),
    Input("btn_confirm", "n_clicks"),
    State("3_dart_avg_current", "children"),
    State("n_visits", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg(n_confirm, curr_avg, n_visits, dart_1, dart_2, dart_3):
    dart_1 = convert_score(dart_1)
    dart_2 = convert_score(dart_2)
    dart_3 = convert_score(dart_3)

    curr_avg = 0 if curr_avg == "_____" else int(curr_avg)
    n_visits = int(n_visits)
    new_avg = float("%.2f" % (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1)))

    return new_avg, str(n_visits + 1)

@app.callback(
    Output("3_dart_avg", "children", allow_duplicate=True),
    Input("btn_confirm", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg_all_time(n_confirm, dart_1, dart_2, dart_3):
    dart_1 = convert_score(dart_1)
    dart_2 = convert_score(dart_2)
    dart_3 = convert_score(dart_3)

    n_visits = read_3_dart_avg(avg=False)
    curr_avg = read_3_dart_avg()
    new_avg = float("%.2f" % (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1)))

    update_3_dart_avg_file(n_visits + 1, new_avg)

    return new_avg

if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=5000)
