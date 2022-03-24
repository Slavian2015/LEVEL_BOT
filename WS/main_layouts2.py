# -*- coding: utf-8 -*-
import json
import sys
import time
from datetime import datetime
from collections import OrderedDict
import dash_bootstrap_components as dbc
from dash import html

sys.path.insert(0, r'/usr/local/WB')


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


def content():
    cont = [
        dbc.Row(style={"width": "100%",
                       "height": "10vh",
                       "minHeight": "10vh",
                       "maxHeight": "10vh",
                       },
                children=[
                    dbc.Col(style={"textAlign": "center",
                                   "margin": "0",
                                   "padding": "0"
                                   },
                            width=6,
                            children=[
                                dbc.Button("KEYS",
                                           href="/keys",
                                           color="primary")]),

                    dbc.Col(style={"textAlign": "center",
                                   "margin": "0",
                                   "padding": "0"
                                   },
                            width=6,
                            children=dbc.Row(
                                [dbc.Col(children=dbc.Input(placeholder="BTCUSDT",
                                                            value="BTCUSDT",
                                                            id="new_symbol",
                                                            size="sm"),
                                         style={"textAlign": "center",
                                                "margin": "0",
                                                "padding": "0"
                                                },
                                         width=3),
                                 dbc.Col(children=dbc.Input(placeholder="2000",
                                                            step=1,
                                                            value=100,
                                                            id="new_amount",
                                                            type='number',
                                                            size="sm"),
                                         style={"textAlign": "center",
                                                "margin": "0",
                                                "padding": "0"
                                                },
                                         width=2),
                                 dbc.Col(children=dbc.Input(placeholder="20",
                                                            id="new_leverage",
                                                            value=1,
                                                            type='number',
                                                            step=1,
                                                            size="sm"),
                                         style={"textAlign": "center",
                                                "margin": "0",
                                                "padding": "0"
                                                },
                                         width=2),
                                 dbc.Col(children=dbc.Input(placeholder="20",
                                                            id="new_timeframe",
                                                            value=1,
                                                            type='number',
                                                            min=1,
                                                            max=60,
                                                            step=1,
                                                            size="sm"),
                                         style={"textAlign": "center",
                                                "margin": "0",
                                                "padding": "0"
                                                },
                                         width=2),
                                 dbc.Col(children=dbc.Button("ADD",
                                                             id="add_new_bot",
                                                             color="success",
                                                             outline=True,
                                                             size="sm"),
                                         style={"textAlign": "center",
                                                "margin": "0",
                                                "padding": "0"
                                                },
                                         width=3)]))]),

        dbc.Row(style={"width": "100%",
                       "height": "89vh",
                       "minHeight": "89vh",
                       "maxHeight": "89vh",
                       # "overflowY": "scroll",
                       "margin": "0",
                       "padding": "0"},
                children=[
                    dbc.Col(style={"textAlign": "center",
                                   "maxHeight": "45vh",
                                   "overflowY": "scroll",
                                   "margin": "0",
                                   "padding": "5px"
                                   },
                            width=6,
                            lg=6,
                            sm=12,
                            xs=12,
                            id="my_left_column",
                            className="no-scrollbars",
                            children=left_column()),

                    dbc.Col(style={"textAlign": "center",
                                   "height": "45vh",
                                   "minHeight": "45vh",
                                   "maxHeight": "45vh",
                                   "overflowY": "hidden",
                                   "margin": "0",
                                   "padding": "5px"},
                            className="no-scrollbars",
                            width=6,
                            lg=6,
                            sm=12,
                            xs=12,
                            children=right_column()
                            ),
                ])]
    return cont


def active_card(symbol=None,
                status=None,
                lot=None,
                leverage=None,
                timeframe=None):
    if symbol:
        my_color, my_text = ("danger", 'STOP') if status == "active" else ("success", "START")

        card = dbc.Card(style={
            "margin": "2px",
            "padding": "0"
        }, children=dbc.CardBody(
            style={
                "margin": "0",
                "padding": "2px",
            },
            children=dbc.Row(style={
                "margin": "0",
                "padding": "0"
            },
                children=[
                    dbc.Col(width=4,
                            style={"text-align": "center"},
                            children=html.A(href=f'https://www.binance.com/ru/futures/{symbol}',
                                        target="blank",
                                        children=symbol)),

                    dbc.Col(width=1,
                            style={"text-align": "center"},
                            children=html.P(f" {lot}", className="card-text")),

                    dbc.Col(width=1,
                            style={"text-align": "center"},
                            children=html.P(f"{leverage} ", className="card-text")),
                    dbc.Col(width=2,
                            style={"text-align": "center"},
                            children=html.P(f"{timeframe} min ", className="card-text")),

                    dbc.Col(width=4,
                            style={"text-align": "left"},
                            children=dbc.Row(style={
                                "margin": "0",
                                "padding": "0"
                            },
                                children=[
                                    dbc.Col(width=6, style={"text-align": "left"},
                                            children=[dbc.Button(my_text,
                                                                 size="sm",
                                                                 id={"type": "symbol_start_button",
                                                                     "index": f'{symbol}_run'}, color=my_color)]),
                                    dbc.Col(width=6, style={"text-align": "right"},
                                            children=[dbc.Button("DEL",
                                                                 size="sm",
                                                                 id={"type": "symbol_del_button",
                                                                     "index": f'{symbol}_run'},
                                                                 outline=True,
                                                                 color="danger")])
                                ]))
                ])
        ))
        return card
    else:
        card = []
        return card


def active_stat_card(date=None,
                     percent=None,
                     symbol=None,
                     profit=None):
    card = dbc.Card(style={
        "margin": "2px",
        "padding": "0"
    }, children=dbc.CardHeader(
        style={
            "margin": "0",
            "padding": "2px"
        },
        children=dbc.Row(style={
            "margin": "0",
            "padding": "0"
        },
            children=[
                dbc.Col(width=3,
                        style={"text-align": "left"},
                        children=html.H6(date)),
                dbc.Col(width=3,
                        style={"text-align": "center"},
                        children=html.A(href=f'https://www.binance.com/ru/futures/{symbol}USDT',
                                        target="blank",
                                        children=symbol)),

                dbc.Col(width=3,
                        style={"text-align": "right"},
                        children=html.P(f" {round(percent, 2)} %", className="card-text")),

                dbc.Col(width=3,
                        style={"text-align": "center"},
                        children=html.P(children=f"{round(profit, 2)} usd ",
                                        style={"color": "lightgreen" if profit > 0 else "#e65a5ab0",
                                               'font-weight': 'bold'})),

            ])
    ))
    return card


def footer_card(total_profit,
                total_percent):
    card = dbc.Row(
        style={"margin": "0",
               "padding": "0"},
        children=[dbc.Col(width=6,
                          style={"text-align": "center"},
                          children=html.H5(children=f"{round(sum(total_percent), 2)} %",
                                           style={"color": "lightgreen" if sum(total_percent) > 0 else "#e65a5ab0",
                                                  'font-weight': 'bold'}
                                           )),
                  dbc.Col(width=6,
                          style={"text-align": "center"},
                          children=html.H5(children=f"{round(sum(total_profit), 2)} usd",
                                           style={"color": "lightgreen" if sum(total_profit) > 0 else "#e65a5ab0",
                                                  'font-weight': 'bold'}))
                  ])

    return card


def header_card(symbols=None, dates=None):
    symbols.append("ALL")

    symbols = set(symbols)
    dates2 = set(dates)

    select_from = dbc.Select(
        id="select_dates_from",
        size="sm",
        value=dates[-1],
        options=[
            {"label": i, "value": i} for i in dates2
        ],
    )

    select_to = dbc.Select(
        id="select_dates_to",
        size="sm",
        value=dates[0],
        options=[
            {"label": i, "value": i} for i in dates2
        ],
    )

    select_symbols = dbc.Select(
        id="select_symbols",
        size="sm",
        value="ALL",
        options=[
            {"label": i, "value": i} for i in symbols
        ],
    )

    card = dbc.Row(
        style={"margin": "0",
               "padding": "0"},

        children=[dbc.Col(width=3,
                          style={"text-align": "center",
                                 "margin": "0",
                                 "padding": "0"},
                          children=select_from),
                  dbc.Col(width=3,
                          style={"text-align": "center",
                                 "margin": "0",
                                 "padding": "0"},
                          children=select_to),
                  dbc.Col(width=3,
                          style={"text-align": "center",
                                 "margin": "0",
                                 "padding": "0"},
                          children=select_symbols),
                  dbc.Col(width=3,
                          style={"text-align": "center",
                                 "margin": "0",
                                 "padding": "0"},
                          children=dbc.Button("filter",
                                              id="add_new_filter",
                                              color="warning",
                                              outline=True,
                                              size="sm"))
                  ])

    return card


def left_column():
    my_list1 = []
    a_file1 = open('/usr/local/WB/data/active.json', "r")
    rools = json.load(a_file1)
    a_file1.close()

    for k, v in rools.items():
        my_list1.append(active_card(
            symbol=k,
            status=v['status'],
            lot=v['lot'],
            leverage=v['leverage'],
            timeframe=v['timeframe']
        ))

    child = dbc.Row(my_list1)
    return [child]


def right_column():
    my_list1 = []
    a_file1 = open('/usr/local/WB/data/statistic.json', "r")
    rools = json.load(a_file1)
    a_file1.close()

    total_dates = []
    total_profit = []
    total_percent = []
    total_symbols = []

    rools = dict(reversed(list(OrderedDict(rools).items())))

    for k, v in rools.items():
        new_date = datetime.strptime(k[:10], '%Y-%m-%d').date().strftime('%d.%m.%Y')
        new_card = active_stat_card(
            date=new_date,
            symbol=v['symbol'][:-4],
            percent=v['percent'],
            profit=v['profit'])

        my_list1.append(new_card)
        total_profit.append(v['profit'])
        total_percent.append(v['percent'])
        total_dates.append(new_date)
        total_symbols.append(v['symbol'][:-4])

    new_footer = footer_card(total_profit, total_percent)

    new_header = header_card(symbols=total_symbols, dates=total_dates)

    card = dbc.Card(
        [
            dbc.CardHeader(new_header),
            dbc.CardBody(
                id="my_right_column",
                style={
                    "height": "32vh",
                    "minHeight": "32vh",
                    "maxHeight": "32vh",
                    "overflowY": "scroll",
                    "margin": "0",
                    "padding": "0"},
                children=my_list1
            ),
            dbc.CardFooter(
                style={"margin": "5px",
                       "padding": "0"},
                children=new_footer,
                id="new_footer"),
        ],
        style={"width": "100%",
               "minHeight": "45vh",
               "maxHeight": "45vh",
               "overflowY": "hidden",
               "margin": "0",
               "padding": "0"
               },
    )

    return [card]


def filter_static(select_dates_from,
                  select_dates_to,
                  select_symbols):

    my_list1 = []
    a_file1 = open('/usr/local/WB/data/statistic.json', "r")
    rools = json.load(a_file1)
    a_file1.close()

    total_dates = []
    total_profit = []
    total_percent = []
    total_symbols = []

    rools = dict(reversed(list(OrderedDict(rools).items())))

    for k, v in rools.items():
        if v['symbol'][:-4] == select_symbols or select_symbols == "ALL":
            datetime_obj_from = datetime.strptime(select_dates_from, '%d.%m.%Y')
            datetime_obj_to = datetime.strptime(select_dates_to, '%d.%m.%Y')

            if datetime_obj_from <= datetime.strptime(k[:10], '%Y-%m-%d') <= datetime_obj_to:

                new_date = datetime.strptime(k[:10], '%Y-%m-%d').date().strftime('%d.%m.%Y')
                new_card = active_stat_card(
                    date=new_date,
                    symbol=v['symbol'][:-4],
                    percent=v['percent'],
                    profit=v['profit'])

                my_list1.append(new_card)
                total_profit.append(v['profit'])
                total_percent.append(v['percent'])
                total_dates.append(new_date)
                total_symbols.append(v['symbol'][:-4])

    my_right_column = my_list1
    new_footer = footer_card(total_profit, total_percent)

    return my_right_column, new_footer



