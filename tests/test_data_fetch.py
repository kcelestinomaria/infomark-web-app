import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_fetch import *
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@patch('openbb.obb.equity.price.historical', return_value=MagicMock(to_df=lambda: pd.DataFrame({'Date': ['2023-01-01'], 'Close': [100]})))
def test_fetch_data(mock_fetch):
    data = data_fetch.fetch_data('Equity', symbol='AAPL', start_date='2023-01-01', end_date='2023-01-31')
    assert not data.empty
    assert 'Date' in data.columns
    assert 'Close' in data.columns

@patch('openbb.obb.equity.search', return_value=MagicMock(to_df=lambda: pd.DataFrame({'symbol': ['AAPL'], 'name': ['Apple Inc.']})))
def test_search_symbols(mock_search):
    results = data_fetch.search_symbols('AAPL')
    assert not results.empty
    assert 'symbol' in results.columns
    assert 'name' in results.columns
