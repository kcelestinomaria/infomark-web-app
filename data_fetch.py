import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Atlas connection string
uri = "mongodb+srv://celestino127:<C0mpa$$i0n127>@cluster0.5qsdpkx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to MongoDB database
db = client['infomark_db']
data_collection = db['data']

def fetch_data(data_type, symbol=None, indicator=None, currency_pair=None, start_date=None, end_date=None, provider='Standard'):
    """Fetches data based on type and filters from MongoDB"""
    query = {"data_type": data_type}
    if symbol:
        query["symbol"] = symbol
    if indicator:
        query["indicator"] = indicator
    if currency_pair:
        query["currency_pair"] = currency_pair
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    if provider != 'Standard':
        query["provider"] = provider

    cursor = data_collection.find(query)
    data = pd.DataFrame(list(cursor))

    # Clean up the DataFrame, if necessary
    if not data.empty:
        data.drop('_id', axis=1, inplace=True)

<<<<<<< HEAD
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
=======
    return data
>>>>>>> 9451902 (Default)
