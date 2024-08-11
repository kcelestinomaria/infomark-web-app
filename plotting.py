import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def plot_data(data, plot_type, data_type):
    # Display the first few rows of the data
    st.write("Data preview:")
    st.write(data.head())

    # Display the column names and data types
    st.write("Column names:", data.columns.tolist())
    st.write("Data types:", data.dtypes.to_dict())

    # Ensure 'Date' column is in datetime format
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        st.write(f"'Date' column converted to datetime. Data type: {data['Date'].dtype}")
    else:
        st.warning('Data missing "Date" column.')
        if plot_type != 'Correlation Matrix':
            st.warning('Switching to Correlation Matrix plot due to missing "Date" column.')
            plot_type = 'Correlation Matrix'

    # Ensure 'Close' column is numeric
    if 'Close' in data.columns:
        data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
        st.write(f"'Close' column converted to numeric. Data type: {data['Close'].dtype}")
    else:
        st.warning('Data missing "Close" column.')
        if plot_type != 'Correlation Matrix':
            st.warning('Switching to Correlation Matrix plot due to missing "Close" column.')
            plot_type = 'Correlation Matrix'

    # Check for missing values in critical columns
    missing_values = data[['Date', 'Close']].isnull().sum()
    st.write("Missing values in critical columns:", missing_values)

    # Plotting based on user selection
    if plot_type == 'Line Graph':
        if 'Date' in data.columns and 'Close' in data.columns and not data[['Date', 'Close']].isnull().values.any():
            st.line_chart(data.set_index('Date')['Close'], use_container_width=True)
        else:
            st.warning('Data does not contain required columns or has missing values for the selected plot type.')
            plot_type = 'Correlation Matrix'

    elif plot_type == 'Simple Table':
        st.dataframe(data)

    elif plot_type == 'Correlation Matrix':
        numeric_cols = data.select_dtypes(include='number')
        if not numeric_cols.empty:
            corr = numeric_cols.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.warning('No numeric columns available to generate a correlation matrix.')

    else:
        st.warning('Invalid plot type or missing data for selected plot type.')
