import os
import base64
import streamlit as st
import pandas as pd
from data_fetch import fetch_data, search_symbols
from plotting import plot_data
from authentication import register_user, authenticate_user, update_user_credentials
# At the beginning of main.py
from initializedb import initialize_database



# Set page config as the very first command
st.set_page_config(page_title="Infomark Financial Dashboard :bar_chart:", layout="wide")

# Initialize the database
initialize_database()

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
    .profile-picture-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }
    .profile-picture-container img {
        border-radius: 50%;
        max-width: 150px;
        max-height: 150px;
    }
    .profile-picture-container h3 {
        margin-top: 10px;
        color: white;
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

def handle_login():
    if st.session_state['authentication_status']:
        return True
    username = st.session_state['username']
    password = st.session_state['password']
    if authenticate_user(username, password):
        st.session_state['authentication_status'] = True
        st.session_state['name'] = username  # Set the name for welcome message
        return True
    return False

def handle_update_credentials():
    if st.session_state['authentication_status']:
        username = st.session_state['username']
        new_username = st.session_state.get('new_username', username)
        new_password = st.session_state.get('new_password', None)
        if update_user_credentials(username, new_username, new_password):
            st.success('Credentials updated successfully!')
            # Update session state
            st.session_state['username'] = new_username
            st.session_state['name'] = new_username
        else:
            st.error('Failed to update credentials.')

def handle_upload_image(uploaded_file):
    if uploaded_file is not None:
        # Ensure the directory exists
        save_dir = './images/'
        os.makedirs(save_dir, exist_ok=True)
        
        # Save file
        save_path = os.path.join(save_dir, f'{st.session_state["username"]}_profile_pic.png')
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success('Profile picture uploaded successfully!')
        return save_path
    return None

def load_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Main function to run the app
def main():
    if st.session_state['authentication_status']:
        # Logged in
        st.sidebar.header('Profile Picture')
        uploaded_file = st.sidebar.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
        profile_pic_path = handle_upload_image(uploaded_file)

        if profile_pic_path:
            # Display the profile picture and user's name at the top of the sidebar
            image_base64 = load_image(profile_pic_path)
            st.sidebar.markdown(f'''
            <div class="profile-picture-container">
                <img src="data:image/png;base64,{image_base64}" />
                <h3>{st.session_state["name"]}</h3>
            </div>
            ''', unsafe_allow_html=True)
        else:
            # Display a placeholder if no image is uploaded
            st.sidebar.markdown(f'''
            <div class="profile-picture-container">
                <h3>{st.session_state["name"]}</h3>
            </div>
            ''', unsafe_allow_html=True)

        st.sidebar.header('Dashboard Navigation')
        if st.sidebar.button('Logout'):
            st.session_state['logout'] = True
            st.session_state['authentication_status'] = False
            st.session_state['username'] = ''
            st.session_state['name'] = ''
            st.session_state['email'] = ''
            # Attempting a workaround for rerun
            st.write("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

        st.write(f'Welcome *{st.session_state["name"]}*')

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
                        st.warning('Data is only available for the table plot type.')
                else:
                    st.warning('No data available for the selected criteria.')

        # Update Credentials Form
        st.sidebar.header('Update Credentials')
        with st.sidebar.form('update_credentials_form'):
            new_username = st.text_input('New Username', value=st.session_state['username'])
            new_password = st.text_input('New Password', type='password')
            if st.form_submit_button('Update Credentials'):
                st.session_state['new_username'] = new_username
                st.session_state['new_password'] = new_password
                handle_update_credentials()

    else:
        # Login / Register
        st.title('Login / Register')

        with st.form('login_form'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            
            if st.form_submit_button('Login'):
                st.session_state['username'] = username
                st.session_state['password'] = password
                if handle_login():
                    st.experimental_rerun()  # Reload the app to show the dashboard
                else:
                    st.error('Username/password is incorrect')

        # Registration
        st.write('No account? Register here:')
        with st.form('register_form'):
            reg_username = st.text_input('Username')
            reg_email = st.text_input('Email')
            reg_password = st.text_input('Password', type='password')
            
            if st.form_submit_button('Register'):
                if register_user(reg_username, reg_email, reg_password):
                    st.success('Registered successfully! Please log in.')
                else:
                    st.error('Username already exists.')

        # Password Reset
        st.write('Forgot Password? Reset here:')
        with st.form('reset_form'):
            reset_username = st.text_input('Username')
            new_password = st.text_input('New Password', type='password')
            
            if st.form_submit_button('Reset Password'):
                if register_user(reset_username, None, new_password):  # Assuming the reset function works like registration
                    st.success('Password reset successfully!')
                else:
                    st.error('Username not found.')

        # Forgot Username
        st.write('Facing Any Issues, or Have Any Feedback To Share? [Contact Support](mailto:support@infomark.com?subject=Forgot%20Username)')

if __name__ == "__main__":
    main()
