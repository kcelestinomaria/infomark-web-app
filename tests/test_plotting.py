import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch
from plotting import *

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_plot_data_line_graph(mocker):
    mock_plot = mocker.patch('plotting.st.line_chart')
    data = pd.DataFrame({'Date': ['2023-01-01'], 'Close': [100]})
    data['Date'] = pd.to_datetime(data['Date'])
    plotting.plot_data(data, 'Line Graph', 'Equity')
    mock_plot.assert_called_once()

def test_plot_data_correlation_matrix(mocker):
    mock_plot = mocker.patch('plotting.st.pyplot')
    data = pd.DataFrame({'Close1': [100, 200], 'Close2': [150, 250]})
    plotting.plot_data(data, 'Correlation Matrix', 'Equity')
    mock_plot.assert_called_once()
