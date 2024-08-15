import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import authentication as auth
from data_fetch import fetch_data, search_symbols
from plotting import plot_data

# Set page config as the very first command
st.set_page_config(page_title="Infomark Financial Dashboard :bar_chart:", layout="wide")

# MongoDB Atlas connection string
uri = "mongodb+srv://celestino127:<C0mpa$$i0n127>@cluster0.5qsdpkx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to MongoDB database
db = client['infomark_db']
users_collection = db['users']
queries_collection = db['queries']

# Apply custom CSS for dark theme
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

# Initialize session state keys
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'name' not in st.session_state:
    st.session_state['name'] = ''
if 'email' not in st.session_state:
    st.session_state['email'] = ''

# Login
if not st.session_state['authentication_status']:
    if auth.login('main'):
        st.session_state['authentication_status'] = True
        st.experimental_rerun()  # Redirect to the main page after login

# Sidebar Menu
with st.sidebar:
    st.title('Infomark Financial Dashboard')
    st.write(f"Welcome, {st.session_state['name']}!")

    if st.session_state['authentication_status']:
        st.header("Search Data")

        # Define filters
        data_type = st.selectbox("Select Data Type", ["Equity", "Crypto", "Commodity", "US Economy Data", "Currency"])
        symbol = st.text_input("Enter Symbol (if applicable)")
        indicator = st.text_input("Enter Indicator (if applicable)")
        currency_pair = st.text_input("Enter Currency Pair (if applicable)")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        provider = st.selectbox("Select Provider", ["Standard", "Custom"])

        if st.button('Fetch Data'):
            data = fetch_data(data_type, symbol=symbol, indicator=indicator, currency_pair=currency_pair, start_date=start_date, end_date=end_date, provider=provider)
            if not data.empty:
                st.write(data)
                plot_type = st.selectbox("Select Plot Type", ["Line Graph", "Simple Table", "Correlation Matrix"])
                plot_data(data, plot_type, data_type)
            else:
                st.error("No data found or error occurred.")
        
        # Save query to MongoDB
        query = {
            'username': st.session_state['username'],
            'data_type': data_type,
            'symbol': symbol,
            'indicator': indicator,
            'currency_pair': currency_pair,
            'start_date': start_date,
            'end_date': end_date,
            'provider': provider
        }
        queries_collection.insert_one(query)
