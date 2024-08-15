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
