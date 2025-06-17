import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import os
import streamlit as st


st.title("Content Tracker")
st.text("Use this free application to track and plan your content")

# Define  the filname
FILENAME = "content_data.csv"


# Define Column structure

COLUMNS = [ 
    "Video Title",
    "Platform",
    "Video Type",
    "Time Posted",
    "Likes",
    "Comments",
    "Shares",
    "Views",
]

# Generate an empty CSV file to store new data
if not os.path.exists(FILENAME):
    empty_df = pd.DataFrame(columns=COLUMNS)
    empty_df.to_csv(FILENAME, index=False)

with st.form("Data Entry Form"):
    st.subheader("Add new post")
    video_title = st.text_input("Video Title")
    platform = st.selectbox("Select platform", ["Instagram", "TikTok", "Flip", "Facebook", "Youtube", "Twitch", "Snapchat"])
    video_type = st.text_input("Video Type")
    time_posted = st.date_input("Date", value = datetime.today())
    likes = st.number_input("Number of likes", min_value = 0)
    comments = st.number_input("Number of Comments", min_value = 0)
    shares = st.number_input("Number of shares", min_value = 0)
    views = st.number_input("Number of views", min_value = 0)
    date_input = st.date_input("Select the date")
    time_input = st.time_input("Select the time")

    # Combine into a datetime object
    datetime_posted = datetime.combine(date_input, time_input)

    # Format it 
    formatted_time_posted = datetime_posted.strftime("%Y-%m-%d %H:%M")

    submit = st.form_submit_button("Add post")

    new_entry = {
        'Video Title': video_title,
        'Platform': platform,
        'Video Type': video_type,
        'Time Posted': formatted_time_posted,
        'Likes':likes,
        'Comments': comments,
        'Shares':shares,
        'Views':views
    }
    if submit:
        # Load existing dataset if exists
        if os.path.exists(FILENAME):
            df = pd.read_csv(FILENAME)
        else:
            df = pd.DataFrame(columns=[col.strip(":") for col in COLUMNS])

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=False)

        # Save back to CSV
        df.to_csv(FILENAME, index=False)
        st.success("New post added successfully!")

        # Show updated data
        st.subheader("All Content Entries")
        st.dataframe(df)


        # ------------------------------------

st.markdown("---")
st.subheader("Update Likes, Shares, or Views")

# Load data if already exists
if os.path.exists(FILENAME):
    df = pd.read_csv(FILENAME)

    # Create a label to uniquely identify rows
if len(df) > 0 and 'Identifier' in df.columns:
    df['Identifier'] = df['Video Title'].astype(str) + " (" + df['Platform'].astype(str) + ")"

    selected_id = st.selectbox("Select a video to update", df['Identifier'])

    filtered_df = df[df['Identifier'] == selected_id]


    # Find the index of the selected row 
    if not filtered_df.empty:
        selected_index = filtered_df.index[0]

    # Get current value or set to 0 
        likes_val = df.loc[selected_index, 'Likes']
        shares_val = df.loc[selected_index, 'Shares']
        views_val = df.loc[selected_index, 'Views']
        comments_val = df.loc[selected_index, 'Comments']

    # Show current values and allow editing 
        new_likes = st.number_input("New Likes", min_value= 0, value=0 if pd.isna(likes_val) else int(likes_val))
        new_shares = st.number_input("New Shares", min_value=0, value=0 if pd.isna(shares_val) else int(shares_val))                             
        new_views = st.number_input("New Views", min_value=0, value=0 if pd.isna(views_val) else int(views_val))
        new_comments = st.number_input("New Comments", min_value=0, value= 0 if pd.isna(comments_val) else int(comments_val))

        if st.button("Update Metrics"):
        # Update selected row 
            df.loc[selected_index, 'Likes'] = new_likes
            df.loc[selected_index, 'Shares'] = new_shares
            df.loc[selected_index, 'Views'] = new_views 

        # Save changes
            df.drop(columns= 'Identifier', inplace=True)
            df.to_csv(FILENAME, index=False)
            st.success("Metrics updated successfully!")
            st.dataframe(df)
    else: 
        st.info("No data found yet. Add posts first.")
else: 
    st.info("There are no posts available to update.")

   
