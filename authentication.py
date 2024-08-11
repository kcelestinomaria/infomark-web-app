import yaml
import streamlit as st
import streamlit_authenticator as stauth

# Load configuration from config.yml
with open('config.yml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Initialize authenticator with configuration from config.yml
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def login(location='main'):
    """
    Handle user login using the authenticator instance.
    """
    return authenticator.login(location=location)

def update_user_details(username, new_name, new_email):
    """
    Update user details (name and email) in the config.yml file.
    """
    try:
        if username in authenticator.credentials['usernames']:
            authenticator.credentials['usernames'][username]['name'] = new_name
            authenticator.credentials['usernames'][username]['email'] = new_email
            # Save updated credentials to config.yml
            with open('config.yml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"An error occurred while updating user details: {e}")
        return False

def register_user(username, email, password):
    """
    Register a new user by adding them to the config.yml file.
    """
    try:
        if username in authenticator.credentials['usernames']:
            return False  # Username already exists
        else:
            # Hash the password before storing
            hashed_password = authenticator.hasher.hash_password(password)
            authenticator.credentials['usernames'][username] = {
                'name': username,
                'email': email,
                'password': hashed_password
            }
            # Save updated credentials to config.yml
            with open('config.yml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            return True
    except Exception as e:
        st.error(f"An error occurred while registering the user: {e}")
        return False

def reset_password(username, new_password):
    """
    Reset the password for a user and update the config.yml file.
    """
    try:
        if username in authenticator.credentials['usernames']:
            # Hash the new password before storing
            hashed_password = authenticator.hasher.hash_password(new_password)
            authenticator.credentials['usernames'][username]['password'] = hashed_password
            # Save updated credentials to config.yml
            with open('config.yml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"An error occurred while resetting the password: {e}")
        return False
