# -*- coding: utf-8 -*-
import os
import sys
import dash_bootstrap_components as dbc
from dash import html

sys.path.insert(0, r'/usr/local/WB')
main_path_data2 = os.path.expanduser('/usr/local/WB/data/')


def my_view():
    layout = [
        html.Div(
            style={
                "height": "100vh",
                "minHeight": "100vh",
                "maxHeight": "100vh",
                "overflowY": "hidden"
            },
            children=content())]
    return layout


def column_left():
    form = dbc.Form(
        [

            dbc.Label("API_key", className="mr-2"),
            dbc.Input(type="password", id="example-api-key_bin", placeholder="Enter API-key"),

            dbc.Label("API_secret", className="mr-2"),
            dbc.Input(type="password", id="example-api-secret_bin", placeholder="Enter API-secret"),

            dbc.Button("Сохранить Binance", id="save_api_bin", color="primary"),
            dbc.Toast(
                [html.P("Done !")],
                id="save_api_bin_toast",
                is_open=False,
                icon="info",
                style={"position": "fixed", "top": 600, "right": 1200, "width": 250},
                duration=2000,
            ),
        ]
    )

    form2 = dbc.Form(
        [
            dbc.Label("API_key", className="mr-2"),
            dbc.Input(type="password", id="example-api-key_telega", placeholder="Enter API-key"),

            dbc.Label("API_secret", className="mr-2"),
            dbc.Input(type="password", id="example-api-secret_telega", placeholder="Enter API-secret"),

            dbc.Button("Сохранить Telega", id="save_api_telega", color="primary"),
            dbc.Toast(
                [html.P("Done !")],
                id="save_api_telega_toast",
                is_open=False,
                icon="info",
                style={"position": "fixed", "top": 600, "right": 1200, "width": 250},
                duration=2000,
            ),
        ]
    )

    cont = [
        dbc.Row(style={"width": "100%",
                       "margin": "0",
                       "margin-bottom": "5px",
                       "padding": "0"},
                children=form),

        dbc.Row(style={"width": "100%",
                       "margin": "0",
                       "margin-bottom": "5px",
                       "padding": "0"},
                children=form2)
    ]

    return cont


def content():

    cont = [
        dbc.Row(style={"width": "100%",
                       "height": "10vh",
                       "minHeight": "10vh",
                       "maxHeight": "10vh",
                       "overflowY": "hidden",
                       "margin": "0",
                       "padding": "0"},
                children=[
                    dbc.Col(style={"textAlign": "center",
                                   "margin": "0",
                                   "padding": "0"
                                   },
                            width=5,
                            children=[
                                dbc.Row(style={"width": "100%",
                                               "margin": "0",
                                               "padding": "0"},
                                        children=[
                                            dbc.Col(style={"textAlign": "center",
                                                           "margin": "0",
                                                           "padding": "0"
                                                           },
                                                    width=6,
                                                    children=[
                                                        dbc.Button("ГЛАВНАЯ",
                                                                   href="/",
                                                                   color="success")])
                                        ])]),
                ],
                ),

        dbc.Row(style={"width": "100%",
                       "height": "89vh",
                       "minHeight": "89vh",
                       "maxHeight": "89vh",
                       "margin": "0",
                       "padding": "0"},
                children=[
                    dbc.Col(style={"textAlign": "center",
                                   "height": "89vh",
                                   "minHeight": "89vh",
                                   "maxHeight": "89vh",
                                   "overflowY": "scroll",
                                   "margin": "0",
                                   "padding": "0"},
                            className="no-scrollbars",
                            width=4,
                            sm=12,
                            lg=4,
                            xs=12,
                            children=column_left()),
                ])]

    return cont