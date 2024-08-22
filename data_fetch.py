# data_fetch.py
import pandas as pd
from openbb import obb
import streamlit as st
import sqlite3

def fetch_data(data_type, symbol="", indicator=None, currency_pair=None, start_date=None, end_date=None, provider="", user_id=None):
    try:
        if provider == "Standard":
            if data_type == 'Equity': # Stocks
                if start_date and end_date:
                    data_daily = obb.equity.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
                else:
                    data_daily = obb.equity.price.historical(symbol=symbol).to_df()
                data = data_daily
            elif data_type == 'Crypto':
                if start_date and end_date:
                    data = obb.crypto.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.crypto.price.historical(symbol=symbol).to_df()
            elif data_type == 'Commodity':
                if start_date and end_date:
                    data = obb.commodity.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.commodity.price.historical(symbol=symbol).to_df()
            elif data_type == 'US Economy Data':
                data = obb.economy.fred_search(["WALCL", "WLRRAL", "WDTGAL", "SP500"]).to_df()
            elif data_type == 'currency':
                if start_date and end_date:
                    data = obb.currency.price.historical(currency_pair=currency_pair, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.currency.price.historical(currency_pair=currency_pair).to_df()
            else:
                return pd.DataFrame()
        else:
            # Handle provider-specific logic
            if data_type == 'Equity':
                if start_date and end_date:
                    data = obb.equity.price.historical(symbol=symbol, provider=provider, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.equity.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'Crypto':
                if start_date and end_date:
                    data = obb.crypto.price.historical(symbol=symbol, provider=provider, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.crypto.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'Commodity':
                if start_date and end_date:
                    data = obb.commodity.price.historical(symbol=symbol, provider=provider, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.commodity.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'US Economy Data':
                data = obb.economy.fred_search(["WALCL", "WLRRAL", "WDTGAL", "SP500"], provider=provider).to_df()
            elif data_type == 'currency':
                if start_date and end_date:
                    data = obb.currency.price.historical(currency_pair=currency_pair, provider=provider, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.currency.price.historical(currency_pair=currency_pair, provider=provider).to_df()
            else:
                log_data_request(user_id=user_id, data_type=data_type, symbol=symbol, indicator=indicator, currency_pair=currency_pair, start_date=start_date, end_date=end_date, provider=provider)
                return pd.DataFrame()
    except Exception as e:
        st.error(f'Error fetching data: {e}')
        return pd.DataFrame()
    return data

def search_symbols(query, user_id=None):
    try:
        # Example for equity symbols, you might need to adjust this based on the provider
        search_results = obb.equity.search(query=query).to_df()
        log_search_history(user_id=user_id, query=query)
        return search_results[['symbol', 'name']]
    except Exception as e:
        st.error(f'Error searching for symbols: {e}')
        return pd.DataFrame()

def log_search_history(user_id, query):
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO SearchHistory (user_id, query) VALUES (?, ?)', (user_id, query))
    conn.commit()
    conn.close()

def log_data_request(user_id, data_type, symbol, indicator, currency_pair, start_date, end_date, provider):
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO DataRequests (user_id, data_type, symbol, indicator, currency_pair, start_date, end_date, provider)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (user_id, data_type, symbol, indicator, currency_pair, start_date, end_date, provider))
    conn.commit()
    conn.close()
