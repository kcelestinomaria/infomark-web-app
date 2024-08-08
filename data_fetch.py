import pandas as pd
from openbb import obb

# Fetch data function
def fetch_data(data_type, symbol="", indicator=None, currency_pair=None, start_date=None, end_date=None, provider=""):
    try:
        if provider == "Standard":
            if data_type == 'Equity':
                data = obb.equity.price.historical(symbol=symbol).to_df()
            elif data_type == 'Crypto':
                data = obb.crypto.price.historical(symbol=symbol).to_df()
            elif data_type == 'Commodity':
                data = obb.commodity.price.historical(symbol=symbol).to_df()
            elif data_type == 'Economic Data':
                data = obb.economic.indicator.historical(indicator=indicator, start_date=start_date, end_date=end_date).to_df()
            elif data_type == 'Forex':
                data = obb.forex.price.historical(currency_pair=currency_pair).to_df()
            else:
                return pd.DataFrame()
        else:
            # Handle specific provider-based logic if not in Standard mode
            if data_type == 'Equity':
                data = obb.equity.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'Crypto':
                data = obb.crypto.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'Commodity':
                data = obb.commodity.price.historical(symbol=symbol, provider=provider).to_df()
            elif data_type == 'Economic Data':
                data = obb.economic.indicator.historical(indicator=indicator, start_date=start_date, end_date=end_date).to_df()
            elif data_type == 'Forex':
                data = obb.forex.price.historical(currency_pair=currency_pair, provider=provider).to_df()
            else:
                return pd.DataFrame()

        return data
    except Exception as e:
        st.error(f'Error fetching data: {e}')
        return pd.DataFrame()
