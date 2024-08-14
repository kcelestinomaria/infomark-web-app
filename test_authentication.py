import pytest
import authentication
from unittest.mock import patch, MagicMock
import yaml
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



@patch('yaml.load', return_value={'credentials': {'usernames': {'test_user': {'name': 'Test User', 'email': 'test@example.com', 'password': 'hashed_password'}}}, 'cookie': {'name': 'test_cookie', 'key': 'test_key', 'expiry_days': 1}, 'pre-authorized': {}})
@patch('authentication.authenticator', autospec=True)
def test_login(mock_authenticator, mock_yaml):
    mock_authenticator.login.return_value = True
    result = authentication.login()
    assert result is True

@patch('authentication.authenticator.credentials', {'usernames': {'test_user': {'name': 'Test User', 'email': 'test@example.com', 'password': 'hashed_password'}}})
def test_update_user_details(mock_authenticator):
    result = authentication.update_user_details('test_user', 'New Name', 'new_email@example.com')
    assert result is True

@patch('authentication.authenticator.credentials', {'usernames': {}})
@patch('authentication.yaml.dump')
def test_register_user(mock_yaml, mock_authenticator):
    result = authentication.register_user('new_user', 'new_email@example.com', 'new_password')
    assert result is True
