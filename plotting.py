<<<<<<< HEAD
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_data(data, plot_type, data_type):
    try:
        if plot_type == 'Line Graph':
            plt.figure(figsize=(10, 6))
            for col in data.columns:
                plt.plot(data.index, data[col], label=col)
            plt.title(f'{data_type} Line Graph')
            plt.xlabel('Date')
            plt.ylabel(data_type)
            plt.legend()
            st.pyplot(plt)
        elif plot_type == 'Simple Table':
            st.write(data)
        elif plot_type == 'Correlation Matrix':
            plt.figure(figsize=(10, 8))
            corr = data.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Matrix')
            st.pyplot(plt)
        else:
            st.error("Unsupported plot type.")
    except Exception as e:
        st.error(f"An error occurred while plotting data: {e}")
=======
import plotly.express as px
import plotly.graph_objects as go

def plot_data(data, plot_type, data_type):
    """Plots data based on the selected plot type"""
    if plot_type == "Line Graph":
        if data_type in ["Equity", "Crypto"]:
            fig = px.line(data, x='date', y='value', title=f"{data_type} Line Graph")
        else:
            fig = go.Figure()
            for column in data.columns:
                if column != 'date':
                    fig.add_trace(go.Scatter(x=data['date'], y=data[column], mode='lines', name=column))
            fig.update_layout(title=f"{data_type} Line Graph")
    elif plot_type == "Simple Table":
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(data.columns)),
            cells=dict(values=[data[col] for col in data.columns])
        )])
        fig.update_layout(title=f"{data_type} Data Table")
    elif plot_type == "Correlation Matrix":
        if 'value' in data.columns:
            corr = data.corr()
            fig = px.imshow(corr, title=f"{data_type} Correlation Matrix")
        else:
            fig = go.Figure()
            fig.update_layout(title=f"No correlation matrix available for {data_type}")
    else:
        fig = go.Figure()
        fig.update_layout(title="Invalid Plot Type")
    fig.show()
>>>>>>> 9451902 (Default)
