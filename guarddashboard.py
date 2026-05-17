import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

st.set_page_config(page_title="Guard Response Portal", layout="wide")

# ====================== LOGIN ======================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Watch Tower Guard Portal Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Admin" and password == "WATCHtower123!@":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect credentials")
    st.stop()

# ====================== SETUP ======================
st.title("🛡️ GUARD RESPONSE PORTAL")
st.caption("WeAreWatchTower.com")

CSV_FILE = "guard_events.csv"

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Event Time", "Response Type", "Arrival Time", "Location", "Event Type", "Notes"])

page = st.sidebar.radio("Navigation", ["Log New Event", "Live Reports", "Performance Charts"])

# ====================== LOG NEW EVENT ======================
if page == "Log New Event":
    st.header("LOG NEW EVENT")
    
    with st.form("log_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Event Date", datetime.now().date())
            time = st.text_input("Event Time", "12:00")
            response_type = st.selectbox("Response Type", ["In Person Guard", "Live Stream (Watch Tower)"])
        with col2:
            arrival = st.text_input("Guard Arrival Time", "12:05")
            location = st.text_input("Location", "Auria")
            event_type = st.selectbox("Event Type", [
                "Alarm", "False Alarm", "Alarm Testing", "User Error",
                "Power Outage", "Signal Lost", "SIGNAL NOT RECEIVED", 
                "Motion", "Door Contact", "Perimeter Breach", "Other"
            ])
            notes = st.text_area("Notes")
        
        if st.form_submit_button("✅ Log Event"):
            new_row = {
                "Date": str(date),
                "Event Time": time,
                "Response Type": response_type,
                "Arrival Time": arrival,
                "Location": location,
                "Event Type": event_type,
                "Notes": notes
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            
            st.success("**✅ EVENT CAPTURED SUCCESSFULLY!**")
            st.balloons()
            st.rerun()

# ====================== LIVE REPORTS with DELETE ======================
elif page == "Live Reports":
    st.header("Recent Events")
    if df.empty:
        st.info("No events logged yet.")
    else:
        for idx in range(len(df)):
            cols = st.columns([7, 1])
            with cols[0]:
                st.write(f"**{df.iloc[idx]['Date']} {df.iloc[idx]['Event Time']}** — {df.iloc[idx]['Response Type']} @ {df.iloc[idx]['Location']} | **{df.iloc[idx]['Event Type']}**")
            with cols[1]:
                if st.button("🗑️", key=f"del_{idx}"):
                    df = df.drop(idx).reset_index(drop=True)
                    df.to_csv(CSV_FILE, index=False)
                    st.success("Event deleted!")
                    st.rerun()
        
        st.subheader("Full Table")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ====================== PERFORMANCE CHARTS ======================
elif page == "Performance Charts":
    st.header("📊 Performance Charts")
    if df.empty:
        st.info("No events logged yet.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Total Events", len(df))
        
        st.subheader("Events by Type")
        type_counts = df['Event Type'].value_counts()
        st.bar_chart(type_counts, height=400)
        
        st.subheader("Distribution by Percentage")
        fig = px.pie(names=type_counts.index, values=type_counts.values, title="Event Type Breakdown")
        st.plotly_chart(fig, use_container_width=True)

st.caption("WeAreWatchTower.com • Guard Response System")
