#main.py
import streamlit as st
import pandas as pd
import authentication as auth
from data_fetch import fetch_data, search_symbols
from plotting import plot_data

# Set page config as the very first command
st.set_page_config(page_title="Infomark Financial Dashboard :bar_chart:", layout="wide")

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
if 'logout' not in st.session_state:
    st.session_state['logout'] = False

# Authentication
if st.session_state['authentication_status']:
    # Logged in
    st.sidebar.header('Dashboard Navigation')
    if st.sidebar.button('Logout'):
        st.session_state['logout'] = True
        auth.authenticator.logout()
        st.session_state['authentication_status'] = False
        st.session_state['username'] = ''
        st.session_state['name'] = ''
        st.session_state['email'] = ''
        # Attempting a workaround for rerun
        st.write("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

    username = st.session_state['username']
    st.write(f'Welcome *{st.session_state["name"]}*')

    # Profile Management
    st.sidebar.header('Profile Management 🛠️')
    with st.sidebar.form('profile_form'):
        st.write('Update your profile details:')
        new_name = st.text_input('New Name', value=st.session_state['name'])
        new_email = st.text_input('New Email', value=st.session_state['email'])
        if st.form_submit_button('Update Profile'):
            if auth.update_user_details(username, new_name, new_email):
                st.session_state['name'] = new_name
                st.session_state['email'] = new_email
                st.success('Profile updated successfully!')
            else:
                st.error('Failed to update profile.')

    # Display content
    st.title('Infomark Financial Dashboard :bar_chart:')
    st.write('Explore data from Infomark across equities, crypto, commodities, economic indicators, and Forex.')

    # Centered Search Bar for Company Ticker Symbol
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    search_query = st.text_input('Search for Ticker Symbol', '', key='search_bar')
    st.markdown('</div>', unsafe_allow_html=True)

    if search_query:
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

        plot_type = st.selectbox('Select Plot Type', ['Line Graph', 'Simple Table'])

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

                # Check columns before plotting
                if 'Date' in data.columns and 'Close' in data.columns:
                    plot_data(data, plot_type, data_type)
                else:
                    st.warning('Data does not contain required columns for the selected plot type.')
            else:
                st.warning('No data available for the selected criteria.')

else:
    # Login / Register
    st.title('Login / Register')

    login_form = st.form('login_form')
    username = login_form.text_input('Username')
    password = login_form.text_input('Password', type='password')
    
    if login_form.form_submit_button('Login'):
        if auth.login(location='main'):
            st.session_state['authentication_status'] = True
            st.session_state['username'] = username
            st.session_state['name'] = username  # Adjust this if necessary
            st.experimental_rerun()  # Reload the app to show the dashboard
        else:
            st.error('Username/password is incorrect')

    # Registration
    st.write('No account? Register here:')
    reg_form = st.form('register_form')
    reg_username = reg_form.text_input('Username')
    reg_email = reg_form.text_input('Email')
    reg_password = reg_form.text_input('Password', type='password')
    
    if reg_form.form_submit_button('Register'):
        if auth.register_user(reg_username, reg_email, reg_password):
            st.success('Registered successfully! Please log in.')
        else:
            st.error('Username already exists.')

    # Password Reset
    st.write('Forgot Password? Reset here:')
    reset_form = st.form('reset_form')
    reset_username = reset_form.text_input('Username')
    new_password = reset_form.text_input('New Password', type='password')
    
    if reset_form.form_submit_button('Reset Password'):
        if auth.reset_password(reset_username, new_password):
            st.success('Password reset successfully!')
        else:
            st.error('Username not found.')

    # Forgot Username
    st.write('Forgot Username? Contact Support.')

    # Forgot Email Verification
    st.write('If you forgot your email, please contact support with your username for verification.')
