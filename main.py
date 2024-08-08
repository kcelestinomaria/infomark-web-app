import streamlit as st
import altair as alt
import pandas as pd
import os
from dotenv import load_dotenv
from openbb import obb

# Load environment variables
load_dotenv()
personal_access_token = os.getenv('PAT')

# Custom theme settings for Streamlit
st.set_page_config(page_title='Infomark Financial Dashboard', page_icon=':bar_chart:', layout='wide')
st.markdown("""
    <style>
    .reportview-container {
        background-color: #000;
        color: #fff;
    }
    .sidebar .sidebar-content {
        background-color: #111;
    }
    .sidebar .sidebar-content .sidebar-menu {
        color: #0f0;
    }
    .css-1r1jkn5 {
        color: #0f0;
    }
    .css-1v0y7v6 {
        background-color: #222;
    }
    .css-1qsox00 {
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

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
    provider = 'yfinance'  # Default provider
    
    if data_type in ['Equity', 'Crypto', 'Commodity', 'Forex']:
        symbol = st.text_input(f'Enter {data_type} Symbol', 'AAPL' if data_type == 'Equity' else 'BTC')
        provider = st.selectbox('Select Provider', ['alpha_vantage', 'cboe', 'fmp', 'intrinio', 'polygon', 'tiingo', 'tmx', 'tradier', 'yfinance'])
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

# Fetch data function
@st.cache_data
def fetch_data(data_type, symbol="", indicator=None, currency_pair=None, start_date=None, end_date=None, provider=""):
    try:
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

# Dark mode theme for Altair charts
def dark_theme():
    return {
        "config": {
            "background": "#000",
            "title": {
                "color": "#0f0"
            },
            "axis": {
                "titleColor": "#0f0",
                "labelColor": "#0f0",
                "gridColor": "#333"
            },
            "legend": {
                "labelColor": "#0f0",
                "titleColor": "#0f0"
            },
            "view": {
                "stroke": "transparent"
            }
        }
    }

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
            if plot_type == 'Line Chart':
                if 'Date' in data.columns and 'Close' in data.columns and data['Close'].dtype in [float, int]:
                    chart = alt.Chart(data).mark_line().encode(
                        x='Date:T',
                        y='Close:Q',
                        color=alt.value('#0f0')
                    ).properties(
                        title=f'{data_type} Line Chart'
                    ).configure(
                        **dark_theme()['config']
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning('Data missing required columns or data types for Line Chart.')
                    
            elif plot_type == 'Candlestick Chart' and all(col in data.columns for col in ['Date', 'Open', 'High', 'Low', 'Close']) and all(data[col].dtype in [float, int] for col in ['Open', 'High', 'Low', 'Close']):
                chart = alt.Chart(data).mark_bar().encode(
                    x='Date:T',
                    y='High:Q',
                    color=alt.value('#0f0'),
                    tooltip=['Date', 'Open', 'High', 'Low', 'Close']
                ).properties(
                    title=f'{data_type} Candlestick Chart'
                ).configure(
                    **dark_theme()['config']
                )
                st.altair_chart(chart, use_container_width=True)
                
            elif plot_type == 'Bar Chart' and 'Volume' in data.columns and data['Volume'].dtype in [float, int]:
                chart = alt.Chart(data).mark_bar().encode(
                    x='Date:T',
                    y='Volume:Q',
                    color=alt.value('#0f0')
                ).properties(
                    title=f'{data_type} Trading Volume'
                ).configure(
                    **dark_theme()['config']
                )
                st.altair_chart(chart, use_container_width=True)
        else:
            st.warning('No data available for the selected criteria.')
