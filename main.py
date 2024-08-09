import streamlit as st
import pandas as pd
from data_fetch import fetch_data, search_symbols
from theme import dark_theme
from plotting import plot_data

# Custom theme settings for Streamlit
dark_theme()

# Streamlit App
st.set_page_config(page_title="Infomark Financial Dashboard :bar_chart:", layout="wide")

# Add custom CSS for dark theme
st.markdown("""
<style>
    .reportview-container {
        background: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #1E1E1E;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #3C3C3C;
        color: white;
        border: 1px solid #666;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid #1E90FF;
    }
</style>
""", unsafe_allow_html=True)

# Main layout
st.title('Infomark Financial Dashboard :bar_chart:')
st.write('Explore data from Infomark across equities, crypto, commodities, economic indicators, and Forex.')

# Centered Search Bar for Company Ticker Symbol
st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
search_query = st.text_input('Search for Ticker Symbol', '', key='search_bar')
st.markdown('</div>', unsafe_allow_html=True)

if search_query is not None:
    try:
        search_results = search_symbols(search_query)
        if not search_results.empty:
            st.write('Search Results:')
            st.dataframe(search_results[['symbol', 'name']])
        else:
            st.warning('No results found for the given search query.')
    except Exception as e:
        st.error(f'An error occurred while searching for the company: {e}')

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

    # Fetch Data Button
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
