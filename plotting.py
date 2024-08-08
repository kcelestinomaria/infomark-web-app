import altair as alt
import pandas as pd
from theme import dark_theme

# Plotting function
def plot_data(data, plot_type, data_type):
    if plot_type == 'Line Chart':
        if 'Date' in data.columns and 'Close' in data.columns and data['Close'].dtype in [float, int]:
            chart = alt.Chart(data).mark_line().encode(
                x='Date:T',
                y='Close:Q',
                color=alt.value('#0f0')
            ).properties(
                title=f'{data_type} Line Chart'
            ).configure(
                **dark_theme()['config']
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning('Data missing required columns or data types for Line Chart.')

    elif plot_type == 'Candlestick Chart' and all(col in data.columns for col in ['Date', 'Open', 'High', 'Low', 'Close']) and all(data[col].dtype in [float, int] for col in ['Open', 'High', 'Low', 'Close']):
        chart = alt.Chart(data).mark_bar().encode(
            x='Date:T',
            y='High:Q',
            color=alt.value('#0f0'),
            tooltip=['Date', 'Open', 'High', 'Low', 'Close']
        ).properties(
            title=f'{data_type} Candlestick Chart'
        ).configure(
            **dark_theme()['config']
        )
        st.altair_chart(chart, use_container_width=True)

    elif plot_type == 'Bar Chart' and 'Volume' in data.columns and data['Volume'].dtype in [float, int]:
        chart = alt.Chart(data).mark_bar().encode(
            x='Date:T',
            y='Volume:Q',
            color=alt.value('#0f0')
        ).properties(
            title=f'{data_type} Trading Volume'
        ).configure(
            **dark_theme()['config']
        )
        st.altair_chart(chart, use_container_width=True)
