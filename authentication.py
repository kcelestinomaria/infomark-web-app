<<<<<<< HEAD
import yaml
import streamlit as st
import streamlit_authenticator as stauth
from pymongo import MongoClient
from pymongo.server_api import ServerApi

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

# MongoDB Atlas connection string
uri = "mongodb+srv://celestino127:<C0mpa$$i0n127>@cluster0.5qsdpkx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to MongoDB database
db = client['infomark_db']
users_collection = db['users']

def login(location='main'):
    """
    Handle user login using the authenticator instance and update session state.
    """
    username, authentication_status, name = authenticator.login(location=location)
    
    if authentication_status:
        # Fetch user details from MongoDB
        user = users_collection.find_one({'username': username})
        if user:
            st.session_state['authentication_status'] = True
            st.session_state['username'] = username
            st.session_state['name'] = name
            st.session_state['email'] = user.get('email', '')
        else:
            st.error("User not found.")
            st.session_state['authentication_status'] = False
            
        return True
    else:
        return False

def register_user(username, email, password):
    """
    Register a new user by adding them to the config.yml file and MongoDB.
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

            # Store user details in MongoDB
            users_collection.insert_one({
                'username': username,
                'name': username,  # Placeholder; user can update later
                'email': email,
                'password': hashed_password  # NOTE: Password stored as hashed
            })

            return True
    except Exception as e:
        st.error(f"An error occurred while registering the user: {e}")
        return False

def update_user_details(username, new_name, new_email):
    """
    Update user details (name and email) in the config.yml file and MongoDB.
    """
    try:
        if username in authenticator.credentials['usernames']:
            authenticator.credentials['usernames'][username]['name'] = new_name
            authenticator.credentials['usernames'][username]['email'] = new_email

            # Save updated credentials to config.yml
            with open('config.yml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            # Update MongoDB user details
            users_collection.update_one(
                {'username': username},
                {'$set': {'name': new_name, 'email': new_email}}
            )
            return True
        else:
            return False
    except Exception as e:
        st.error(f"An error occurred while updating user details: {e}")
        return False

def reset_password(username, new_password):
    """
    Reset the password for a user and update the config.yml file and MongoDB.
    """
    try:
        if username in authenticator.credentials['usernames']:
            # Hash the new password before storing
            hashed_password = authenticator.hasher.hash_password(new_password)
            authenticator.credentials['usernames'][username]['password'] = hashed_password

            # Save updated credentials to config.yml
            with open('config.yml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            # Update MongoDB password
            users_collection.update_one(
                {'username': username},
                {'$set': {'password': hashed_password}}
            )
            return True
        else:
            return False
    except Exception as e:
        st.error(f"An error occurred while resetting the password: {e}")
        return False
=======
>>>>>>> 9451902 (Default)
