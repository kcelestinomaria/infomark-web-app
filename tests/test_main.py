import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import main

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Mock the Streamlit functions and modules used in main.py
@pytest.fixture
def mock_auth():
    with patch('authentication.authenticator') as mock_authenticator:
        yield mock_authenticator

def test_authentication_status(mock_auth):
    with patch('streamlit.session_state', {'authentication_status': True, 'username': 'test_user', 'name': 'Test User', 'email': 'test@example.com'}):
        main.main()
        assert 'Welcome *Test User*' in st._latest_message()

@patch('authentication.authenticator.logout')
def test_logout(mock_logout):
    with patch('streamlit.session_state', {'authentication_status': True, 'username': 'test_user'}):
        with patch('streamlit.button', return_value=True):
            main.main()
        mock_logout.assert_called_once()
        assert 'authentication_status' not in st.session_state

def test_search_symbols(mocker):
    mock_search_symbols = mocker.patch('data_fetch.search_symbols', return_value=pd.DataFrame({'symbol': ['AAPL'], 'name': ['Apple Inc.']}))
    st.session_state['authentication_status'] = True
    st.text_input = MagicMock(return_value='AAPL')
    main.main()
    assert 'Search Results:' in st._latest_message()
