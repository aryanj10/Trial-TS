import streamlit as st
import pandas as pd
import numpy as np
import math

# Title for the web app
st.title("Trade Data & Client Intro Analysis")

# Step 1: File uploaders for two CSV files
st.subheader("Upload the CSV files:")
uploaded_trade_data = st.file_uploader("Choose the Trade Data CSV file", type="csv")
uploaded_intro_code = st.file_uploader("Choose the Client Intro Data CSV file", type="csv")

# Step 2: Process the uploaded files if both are provided
if uploaded_trade_data is not None and uploaded_intro_code is not None:
    # Read the uploaded CSV files
    trade_data = pd.read_csv(uploaded_trade_data)
    intro_code = pd.read_csv(uploaded_intro_code)

    # Display previews of the data
    st.write("Trade Data Preview:")
    st.dataframe(trade_data.head())

    st.write("Intro Code Data Preview:")
    st.dataframe(intro_code.head())

    # Merging the trade data with intro code on 'ClientCode' and 'Client Code'
    trade_data_merge = trade_data.merge(intro_code, left_on='ClientCode', right_on='Client Code')

    # Display the merged data
    st.subheader("Merged Data")
    st.dataframe(trade_data_merge.head())

    # Create 'Quarter' column based on 'TradeDate'
    quarter = []
    for i in trade_data_merge['TradeDate']:
        if (int(i[3:5]) == 12) or (int(i[3:5]) == 11) or (int(i[3:5]) == 10):
            quarter.append('Q3')
        elif (int(i[3:5]) == 9) or (int(i[3:5]) == 8) or (int(i[3:5]) == 7):
            quarter.append('Q2')
        elif (int(i[3:5]) == 6) or (int(i[3:5]) == 5) or (int(i[3:5]) == 4):
            quarter.append('Q1')
        elif (int(i[3:5]) == 1) or (int(i[3:5]) == 2) or (int(i[3:5]) == 3):
            quarter.append('Q4')
        else:
            quarter.append('Error')
    
    trade_data_merge['Quarter'] = quarter
    st.write("Data with Quarter column:")
    st.dataframe(trade_data_merge.head())

    # Filter data where 'Brok Type' is 20632 and 'Intro by' is not null
    intro_present = trade_data_merge[(trade_data_merge['Brok Type'] == 20632) & (trade_data_merge['Intro by'].notnull())]

    # Create a new column 'Brok Give' for brokerage calculation (25%)
    intro_present['Brok give'] = intro_present['Brok'] * 0.25
    st.subheader("Clients with Introducer")
    st.dataframe(intro_present.head())

    # Calculate and display total brokerage to give
    intro_present_total = intro_present['Brok give'].sum()
    st.write(f"Total Brokerage to give (25%): {intro_present_total}")

    # Export intro_present data to CSV
    intro_present.to_csv('New_file_1.csv', index=False)
    st.write("Intro Client data saved to 'New_file_1.csv'")

    # Filter data where 'Brok Type' is 20632 and 'Intro by' is null
    intro_not_present = trade_data_merge[(trade_data_merge['Brok Type'] == 20632) & (trade_data_merge['Intro by'].isna())]
    intro_not_present_total = intro_not_present['Brok'].sum()
    st.subheader("Clients without Introducer")
    st.dataframe(intro_not_present.head())

    # Display total brokerage for clients without introducer
    st.write(f"Total Brokerage (Direct Clients): {intro_not_present_total}")

    # Display quarterly totals
    fy_q = ['Q1', 'Q2', 'Q3', 'Q4']
    for i in fy_q:
        st.subheader(f"Quarterly Totals for {i}")

        # Introduced clients (25% brokerage)
        q_data_present = intro_present[intro_present['Quarter'] == i]
        intro_present_total_q = math.ceil(q_data_present['Brok give'].sum())
        st.write(f"Intro Client (25%) {i} Total: {intro_present_total_q}")

        # Direct clients (full brokerage)
        q_data_not_present = intro_not_present[intro_not_present['Quarter'] == i]
        intro_not_present_total_q = math.ceil(q_data_not_present['Brok'].sum())
        st.write(f"Direct Client {i} Total: {intro_not_present_total_q}")
        st.write("\n")

