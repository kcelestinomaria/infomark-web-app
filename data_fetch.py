# data_fetch.py
import pandas as pd
from openbb import obb

# Fetch data function
def fetch_data(data_type, symbol="", indicator=None, currency_pair=None, start_date=None, end_date=None, provider=""):
    try:
        if provider == "Standard":
            if data_type == 'Equity': # Stocks
                # Historical Market prices for equity markets typically come
                # in the form of OHLC+V - open, high, low, close, and volume
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
                
                # Publishes data from the Federal Reserve(FRED)
                # WALCL (All Liabilities) - WLRRAL (RRP) - WDTGAL (TGA)
                # We have picked one economic indicator for US Economy Data, and that is the USD Liquidity Index

                data = obb.economy.fred_search(["WALCL", "WLRRAL", "WDTGAL", "SP500"]) #to_df()
            elif data_type == 'Forex':
                if start_date and end_date:
                    data = obb.forex.price.historical(currency_pair=currency_pair, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.forex.price.historical(currency_pair=currency_pair).to_df()
            else:
                return pd.DataFrame()
        else:
            # Handle specific provider-based logic if not in Standard mode
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
                data = obb.economy.fred_search(["WALCL", "WLRRAL", "WDTGAL", "SP500"]) #to_df()
            elif data_type == 'Forex':
                if start_date and end_date:
                    data = obb.forex.price.historical(currency_pair=currency_pair, provider=provider, start_date=start_date, end_date=end_date).to_df()
                else:
                    data = obb.forex.price.historical(currency_pair=currency_pair, provider=provider).to_df()
            else:
                return pd.DataFrame()

        return data
    except Exception as e:
        st.error(f'Error fetching data: {e}')
        return pd.DataFrame()


def search_symbols(query):
    """
    Search for ticker symbols using the SEC with OpenBB.
    """
    try:
        if query:
            # Search for the provided query
            results = obb.equity.search(query, provider="sec")
        else:
            # Search for all symbols if no query is provided
            results = obb.equity.search("", provider="sec")

        # Convert results to DataFrame
        df_results = results.to_df()
        return df_results
    except Exception as e:
        print(f'Error fetching symbols from SEC: {e}')
        return pd.DataFrame()