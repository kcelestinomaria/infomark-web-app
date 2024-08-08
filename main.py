import streamlit as st
import pandas as pd
from data_fetch import fetch_data
from theme import dark_theme
from plotting import plot_data

# Load environment variables
# ... (Load environment variables code here)

# Custom theme settings for Streamlit
dark_theme()

# Streamlit App
st.title('Infomark Financial Dashboard :bar_chart:')
st.write('Explore data from Infomark across equities, crypto, commodities, economic indicators, and Forex.')

# Sidebar for user input
with st.sidebar:
    st.header('User Input 🛠️')
    data_type = st.selectbox('Select Data Type', ['Equity', 'Crypto', 'Commodity', 'Economic Data', 'Forex'])

    symbol = None
    indicator = None
    currency_pair = None
    provider = st.selectbox('Select Provider', ['Standard', 'alpha_vantage', 'cboe', 'fmp', 'intrinio', 'polygon', 'tiingo', 'tmx', 'tradier', 'yfinance'])

    if data_type in ['Equity', 'Crypto', 'Commodity', 'Forex']:
        symbol = st.text_input(f'Enter {data_type} Symbol', 'AAPL' if data_type == 'Equity' else 'BTC')
    if data_type == 'Economic Data':
        indicator = st.text_input('Enter Economic Indicator', 'GDP')

    try:
        start_date = pd.to_datetime(st.date_input('Start Date', pd.to_datetime('2023-01-01')))
        end_date = pd.to_datetime(st.date_input('End Date', pd.to_datetime('2023-12-31')))
    except ValueError:
        st.error('Invalid date format. Please use YYYY-MM-DD.')
        start_date, end_date = None, None

    plot_type = st.selectbox('Select Plot Type', ['Line Chart', 'Candlestick Chart', 'Bar Chart', 'Simple Table'])

    if start_date is not None and end_date is not None and start_date > end_date:
        st.error('Start date must be before end date.')

# Main content area
if st.button('Fetch Data 📊'):
    if start_date is None or end_date is None:
        st.warning('Please enter valid start and end dates.')
    else:
        with st.spinner('Fetching data...'):
            data = fetch_data(data_type, symbol=symbol, indicator=indicator, currency_pair=currency_pair, start_date=start_date, end_date=end_date, provider=provider)

        if not data.empty:
            st.subheader(f'{data_type} Data 📈')

            # Display data table
            if plot_type == 'Simple Table':
                st.dataframe(data)

            # Plotting based on user selection
            plot_data(data, plot_type, data_type)
        else:
            st.warning('No data available for the selected criteria.')
