from os import system, name
import pandas as pd
import requests
import sys
import ast
import json

ENDPOINT = "https://www.alphavantage.co/query"
# api_key = "XTL1KGHHYG2BABLZ"
api_key = input("Welcome to Alpha Advantage!\nTo Start insert your API Key: ")


def api_call(function, symbol):
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
    }
    response = requests.get(ENDPOINT, params=params)
    # print(response.text)
    if function == "GLOBAL_QUOTE":
        data = response.json()["Global Quote"]
        df = pd.DataFrame([data])
        print('\n\n')
        print(df.to_markdown(index=False))
        print('\n\n')
    else:
        data = response.json()["Meta Data"]
        df = pd.DataFrame([data])
        print(df.to_markdown(tablefmt='grid'))

        if function == "TIME_SERIES_DAILY":
            data = response.json()["Time Series (Daily)"]
        elif function == "TIME_SERIES_WEEKLY":
            data = response.json()["Weekly Time Series"]
        elif function == "TIME_SERIES_MONTHLY":
            data = response.json()["Monthly Time Series"]

        df = pd.DataFrame.from_dict(data, orient='index')
        print('\n\n')
        print(df.to_markdown(tablefmt='grid'))
        print('\n\n')


def api_call_indicators(function, symbol, interval, time_period, series_type):
    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "apikey": api_key,
    }
    response = requests.get(ENDPOINT, params=params)
    # print(response.text)
    data = response.json()["Meta Data"]
    df = pd.DataFrame([data])
    print(df.to_markdown(tablefmt='grid'))

    if function == "sma":
        data = response.json()["Technical Analysis: SMA"]
    elif function == "ema":
        data = response.json()["Technical Analysis: EMA"]

    df = pd.DataFrame.from_dict(data, orient='index')
    print('\n\n')
    print(df.to_markdown(tablefmt='grid'))
    print('\n\n')


def search(keywords):
    search_params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "apikey": api_key,
    }
    response = requests.get(ENDPOINT, params=search_params)
    data = response.json()["bestMatches"][0:]
    df = pd.DataFrame(data)
    print('\n\n')
    print(df.to_markdown(tablefmt='grid'))
    print('\n\n')


def menu_options():
    menu_2 = input(
        'Select one option: \n 1 - Main Menu \n 2 - Exit \n (insert a number)=>: ')
    if menu_2 == '1':
        main_menu()
    elif menu_2 == '2':
        sys.exit()


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main_menu():
    clear()
    print(''' 
 █████  ██      ██████  ██   ██  █████      ██    ██  █████  ███    ██ ████████  █████   ██████  ███████ 
██   ██ ██      ██   ██ ██   ██ ██   ██     ██    ██ ██   ██ ████   ██    ██    ██   ██ ██       ██      
███████ ██      ██████  ███████ ███████     ██    ██ ███████ ██ ██  ██    ██    ███████ ██   ███ █████   
██   ██ ██      ██      ██   ██ ██   ██      ██  ██  ██   ██ ██  ██ ██    ██    ██   ██ ██    ██ ██      
██   ██ ███████ ██      ██   ██ ██   ██       ████   ██   ██ ██   ████    ██    ██   ██  ██████  ███████ 
                                                                                                         
                                                                                                         
''')
    option = input('Select one of the following options: \n\n 1 - Search company symbol \n 2 - display historical prices daily, weekly, monthly \n 3 - display current quote \n 4 - indicator results in grid \n\n (insert a number)=>: ')

    if option == '1':
        clear()
        keywords = input(
            'Insert company name to search it symbol and details: ')
        search(keywords)
        menu_options()

    elif option == '2':
        clear()
        print('HISTORICAL PRICES')
        symbol = input('Insert the company Symbol: ')
        prices_option = input(
            '\n Select one of the following options: \n 1 - Daily \n 2 - Weekly \n 3 - Monthly \n (insert a number)=>:  ')
        if prices_option == '1':
            api_call("TIME_SERIES_DAILY", symbol)
            menu_options()
        if prices_option == '2':
            api_call("TIME_SERIES_WEEKLY", symbol)
            menu_options()
        if prices_option == '3':
            api_call("TIME_SERIES_MONTHLY", symbol)
            menu_options()

    elif option == '3':
        clear()
        print('CURRENT QUOTE')
        symbol = input('Insert the company Symbol: ')
        api_call("GLOBAL_QUOTE", symbol)
        menu_options()

    elif option == '4':
        clear()
        print('INDICATORS')
        symbol = input('Insert the company Symbol: ')
        function = input('Insert one of the indicators (SMA or EMA): ').lower()
        interval = input(
            'Insert the interval (1min, 5min, 15min, 30min, 60min, daily, weekly, monthly): ')
        time_period = input('Insert a time period (e.g. 60, 200): ')
        series_type = input('Insert the type (close, open, high, low:) ')
        api_call_indicators(function, symbol, interval,
                            time_period, series_type)
        menu_options()


main_menu()
