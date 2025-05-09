import streamlit as st
import requests

BASE_URL = "http://localhost:5001/api"

def main():
    st.title("🚨 Emergency Access")

    id_number = st.text_input("Enter Citizen ID")
    pin = st.text_input("Enter 4-digit Emergency PIN", type="password", max_chars=4)

    if st.button("Access Emergency Info"):
        try:
            payload = {"pin": pin, "idNumber": id_number}
            res = requests.post(f"{BASE_URL}/emergency/access", json=payload)
            if res.status_code == 200:
                citizen = res.json()
                st.success("✅ Access Granted")
                st.markdown(f"### 👤 Name: {citizen['name']}")
                st.write(f"🩺 Blood Type: {citizen.get('bloodType', 'N/A')}")
                st.write(f"💊 Medications: {citizen.get('medications', 'N/A')}")
                st.write(f"🌡️ Allergies: {citizen.get('allergies', 'N/A')}")
            elif res.status_code == 401:
                st.error("❌ Invalid PIN")
            elif res.status_code == 404:
                st.error("❌ Citizen not found")
            else:
                st.error("❌ Something went wrong")
        except Exception as e:
            st.error(f"❌ Error: {e}")
