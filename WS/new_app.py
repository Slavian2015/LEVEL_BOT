import warnings
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import flask
import json
import os
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

import subprocess
import keys_layouts
import main_layouts2

warnings.filterwarnings("ignore")

main_path_data = os.path.expanduser('/usr/local/WB/data/')

external_stylesheets = [dbc.themes.DARKLY]
app = flask.Flask(__name__)
dash_app = dash.Dash(__name__,
                     url_base_pathname="/",
                     suppress_callback_exceptions=True,
                     server=app,
                     external_stylesheets=external_stylesheets,
                     meta_tags=[
                         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                     ])

dash_app.title = 'LEVELS'

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div("TEST", id="hidden_port", style={'display': 'none'})
])


@dash_app.callback(Output('page-content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_layouts2.my_view()
    elif pathname == '/keys':
        return keys_layouts.my_view()
    else:
        return "404"


# ###############################    UPDATE KEYS    ##################################

@dash_app.callback([Output('save_api_bin_toast', 'is_open')],
                   [Input('save_api_bin', 'n_clicks')],
                   [State('example-api-key_bin', 'value'),
                    State('example-api-secret_bin', 'value')])
def trigger_balance2(n1, api_key, api_secret):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')
    if button_id[0] == 'save_api_bin':
        if not api_key or not api_secret:
            raise PreventUpdate
        else:
            main_path_settings = f'{main_path_data}settings.json'
            a_file1 = open(main_path_settings, "r")
            rools = json.load(a_file1)
            a_file1.close()

            with open(main_path_settings, "w") as f:
                rools["api_key"] = api_key
                rools["api_secret"] = api_secret

                json.dump(rools, f, indent=4)
        return [True]
    else:
        raise PreventUpdate


@dash_app.callback([Output('save_api_telega_toast', 'is_open')],
                   [Input('save_api_telega', 'n_clicks')],
                   [State('example-api-key_telega', 'value'),
                    State('example-api-secret_telega', 'value')])
def trigger_balance2(n1, api_key, api_secret):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')
    if button_id[0] == 'save_api_telega':
        if not api_key or not api_secret:
            raise PreventUpdate
        else:
            main_path_settings = f'{main_path_data}settings.json'
            a_file1 = open(main_path_settings, "r")
            rools = json.load(a_file1)
            a_file1.close()

            with open(main_path_settings, "w") as f:
                rools["api_key_t"] = api_key
                rools["api_secret_t"] = api_secret
                json.dump(rools, f, indent=4)
        return [True]
    else:
        raise PreventUpdate


@dash_app.callback(
    [Output({'type': 'symbol_start_button', 'index': MATCH}, 'color'),
     Output({'type': 'symbol_start_button', 'index': MATCH}, 'children')],
    [Input({'type': 'symbol_start_button', 'index': MATCH}, 'n_clicks')])
def toggle_modal3(n):
    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]
    if not button:
        raise PreventUpdate
    else:
        if type(button) is str:
            button = json.loads(button.replace("'", "\""))
        if button["type"] == 'symbol_start_button':
            main_path_settings = f'{main_path_data}active.json'
            a_file1 = open(main_path_settings, "r")
            rools2 = json.load(a_file1)
            a_file1.close()

            print(f'START BTN : {button["index"][:-4]}')
            if rools2[button["index"][:-4]]['status'] == 'active':
                rools2[button["index"][:-4]]['status'] = 'disabled'
                f = open(main_path_settings, "w")
                json.dump(rools2, f, indent=4)
                f.close()

                pid = subprocess.Popen(["python",
                                        "/usr/local/WB/WS/stop_bot.py",
                                        f"--leverage={rools2[button['index'][:-4].upper()]['leverage']}",
                                        f"--timeframe={rools2[button['index'][:-4].upper()]['timeframe']}min",
                                        f"--amount={rools2[button['index'][:-4].upper()]['lot']}",
                                        f"--symbol={button['index'][:-4].upper()}"]).pid

                return ["success", "START"]
            else:
                rools2[button["index"][:-4].upper()]['status'] = 'active'
                f = open(main_path_settings, "w")
                json.dump(rools2, f, indent=4)
                f.close()

                with open(f'{main_path_data}running.json', "r") as new_f:
                    new_run = json.load(new_f)

                pid = subprocess.Popen(["python",
                                        "/usr/local/WB/WS/start_bot.py",
                                        f"--leverage={rools2[button['index'][:-4].upper()]['leverage']}",
                                        f"--timeframe={rools2[button['index'][:-4].upper()]['timeframe']}min",
                                        f"--amount={rools2[button['index'][:-4].upper()]['lot']}",
                                        f"--symbol={button['index'][:-4].upper()}"]).pid

                with open(main_path_settings, "w") as f:
                    json.dump(rools2, f, indent=4)

                with open(f'{main_path_data}running.json', "w") as f:
                    new_run[button["index"][:-4].upper()] = pid
                    json.dump(new_run, f, indent=4)

                return ["danger", "STOP"]
        else:
            raise PreventUpdate


# ###############################    ADD / DEL NEW BOT    ##################################
@dash_app.callback(
    output=[Output("my_left_column", 'children')],
    inputs=[Input({'type': 'symbol_del_button', 'index': ALL}, 'n_clicks'),
            Input('add_new_bot', 'n_clicks')],
    state=[State('new_symbol', 'value'),
           State('new_amount', 'value'),
           State('new_leverage', 'value'),
           State('new_timeframe', 'value')])
def toggle_del(n, n2, new_symbol, new_amount, new_leverage, new_timeframe):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')
    if button_id[0] == 'add_new_bot':
        if not all([new_symbol, new_amount, new_leverage, new_timeframe]):
            raise PreventUpdate
        else:
            a_file1 = open(main_path_data + "active.json", "r")
            rools = json.load(a_file1)
            a_file1.close()

            with open(main_path_data + "active.json", "w") as f:
                rools[new_symbol] = {"status": "disabled",
                                     "lot": new_amount,
                                     "leverage": new_leverage,
                                     "timeframe": new_timeframe}
                json.dump(rools, f, indent=4)
            return main_layouts2.left_column()

    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]

    if not button:
        raise PreventUpdate
    else:
        if type(button) is str:
            button = json.loads(button.replace("'", "\""))

        if button["type"] == 'symbol_del_button':
            my_symbol = button["index"][:-4]

            main_path_settings = f'{main_path_data}active.json'
            a_file1 = open(main_path_settings, "r")
            rools2 = json.load(a_file1)
            a_file1.close()
            rools2.pop(my_symbol.upper(), None)
            f = open(main_path_settings, "w")
            json.dump(rools2, f, indent=4)
            f.close()
            return main_layouts2.left_column()
        else:
            raise PreventUpdate


# ###############################    FILTER STATISTICS    ##################################
@dash_app.callback([Output('my_right_column', 'children'),
                    Output('new_footer', 'children')],
                   [Input('add_new_filter', 'n_clicks')],
                   [State('select_dates_from', 'value'),
                    State('select_dates_to', 'value'),
                    State('select_symbols', 'value')])
def trigger_balance2(n1, select_dates_from, select_dates_to, select_symbols):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')
    if button_id[0] == 'add_new_filter':

        print(select_dates_from, select_dates_to, select_symbols)
        my_right_column, new_footer = main_layouts2.filter_static(select_dates_from, select_dates_to, select_symbols)

        return my_right_column, new_footer
    else:
        raise PreventUpdate


if __name__ == '__main__':
    dash_app.run_server(host="0.0.0.0",
                        # host="172.22.0.4",
                        port=3039,
                        debug=False)
