import pandas as pd
from openbb import obb
import streamlit as st

def fetch_data(data_type, symbol="", indicator=None, currency_pair=None, start_date=None, end_date=None, provider=""):
    try:
        if provider == "Standard":
            if data_type == 'Equity':  # Stocks
                data = obb.equity.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
            elif data_type == 'Crypto':
                data = obb.crypto.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
            elif data_type == 'Commodity':
                data = obb.commodity.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
            elif data_type == 'US Economy Data':
                data = obb.economy.fred_search(["WALCL", "WLRRAL", "WDTGAL", "SP500"]).to_df()
            elif data_type == 'Currency':
                data = obb.fx.price.historical(symbol=symbol, start_date=start_date, end_date=end_date).to_df()
            else:
                data = pd.DataFrame()
        elif provider == "Custom":
            # Implement custom provider data fetching
            data = pd.DataFrame()  # Placeholder
        else:
            data = pd.DataFrame()
        
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()

def search_symbols(search_term):
    try:
        results = obb.search(search_term)
        return results
    except Exception as e:
        st.error(f"An error occurred while searching for symbols: {e}")
        return pd.DataFrame()
