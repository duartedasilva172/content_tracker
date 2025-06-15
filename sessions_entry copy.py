import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import os


# Add title and short description
st.title("Sessions Tracker")
st.text("Track your sessions, trips, expenses, and earnings as a courier, enter the datapoints you want to collect and the tracker will generate a CSV file ready for you to analyze!")

# File path where the data will be saved 
SESSION_FILE = "data/uber_sessions_data.csv"

# If the file exisrs, load it: otherwise, create an empty dataframe

sessions_df = pd.read_csv(SESSION_FILE)
sessions_df

# ---------- Session Entry Form -----------

with st.form("session_form"):
    st.subheader("Add New Session")
    session_id = st.text_input("Session ID")
    session_date = st.date_input("Date", value=datetime.today())
    start_time = st.time_input("Start Time", value=datetime.now().time())
    end_time = st.time_input ("End Time", value=datetime.now().time())
    trips = st.number_input("Number of Trips", min_value=0)
    earned = st.number_input("Total Earned ($)", min_value=0.0)
    device = st.text_input("Device Used")

    submit = st.form_submit_button("Add Session")

    if submit:
        start_dt = datetime.combine(session_date, start_time)
        end_dt = datetime.combine(session_date, end_time)
        
        if end_dt < start_dt: 
            end_dt += timedelta(days=1)

        duration = end_dt - start_dt
        shift_length_hrs = round(duration.total_seconds() / 3600, 2)
        
        new_entry = { 
        'session_id': session_id,
        'date': session_date,
        'start_time': start_time.strftime("%H:%M"),
        'end_time': end_time.strftime("%H:%M"),
        'shift_length_hrs': shift_length_hrs,
        'trips': trips,
        'total_earned': earned, 
        'device_used': device
    }
    
        new_row = pd.DataFrame([new_entry])
        sessions_df = pd.concat([sessions_df, new_row], ignore_index=True)
        sessions_df.to_csv(SESSION_FILE, index=False) 
        st.success("Session added successfully")