import streamlit as st
from hospital_view import main as hospital_main
from citizen_view import main as citizen_main
from emergency_view import main as emergency_main

st.set_page_config(page_title="Health Data Hub", layout="wide")

st.title("🚀 Health Data Hub")
role = st.selectbox("Select your role to continue:", ["Select", "🏥 Hospital", "👤 Citizen", "🚨 Emergency"])

if role == "🏥 Hospital":
    hospital_main()
elif role == "👤 Citizen":
    citizen_main()
elif role == "🚨 Emergency":
    emergency_main()
else:
    st.info("Please select a role to get started.")

