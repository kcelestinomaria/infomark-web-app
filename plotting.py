import altair as alt
import pandas as pd
import streamlit as st
from theme import dark_theme

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

    elif plot_type == 'Candlestick Chart' and all(col in data.columns for col in ['Date', 'Open', 'High', 'Low', 'Close']):
        base = alt.Chart(data).encode(
            x='Date:T'
        )
        
        # Create the open-high and low-close bars
        rules = base.mark_rule().encode(
            y='Open:Q',
            y2='Close:Q',
            color=alt.condition(
                alt.datum.Open < alt.datum.Close,
                alt.value('green'),
                alt.value('red')
            )
        )
        
        # Create the high-low bars
        bars = base.mark_bar().encode(
            y='High:Q',
            y2='Low:Q',
            color=alt.condition(
                alt.datum.Open < alt.datum.Close,
                alt.value('green'),
                alt.value('red')
            )
        )
        
        chart = rules + bars
        chart = chart.properties(
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

    elif plot_type == 'Simple Table':
        st.dataframe(data)
    else:
        st.warning('Invalid plot type or missing data for selected plot type.')
