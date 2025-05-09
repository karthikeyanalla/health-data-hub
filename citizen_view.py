import streamlit as st
import requests

BASE_URL = "http://localhost:5001/api"

def main():
    st.title("👤 Citizen Login")

    id_number = st.text_input("Enter your ID Number")
    dob = st.date_input("Enter your Date of Birth")

    if st.button("View My Records"):
        try:
            response = requests.get(f"{BASE_URL}/citizens/idNumber/{id_number}")
            if response.status_code == 200:
                citizen = response.json()
                if citizen["dob"].split("T")[0] == dob.isoformat():
                    st.success("✅ Record found")
                    st.markdown(f"### 👤 Name: {citizen['name']}")
                    st.write(f"📧 Email: {citizen['email']}")
                    st.write(f"📞 Phone: {citizen['phone']}")
                    st.write(f"🩺 Blood Type: {citizen.get('bloodType', 'N/A')}")
                    st.write(f"💊 Medications: {citizen.get('medications', 'N/A')}")
                    st.write(f"🌡️ Allergies: {citizen.get('allergies', 'N/A')}")

                    st.markdown("### 📄 Uploaded Files")
                    if citizen["uploadedFiles"]:
                        for file in citizen["uploadedFiles"]:
                            file_name = file.get("fileName", "Unnamed")
                            file_type = file.get("fileType", "Unknown")
                            file_url = f"{BASE_URL.replace('/api', '')}/uploads/{file['filePath'].split('/')[-1]}"
                            st.write(f"**{file_name}** ({file_type})")
                            st.markdown(f"[📥 Download File]({file_url})", unsafe_allow_html=True)
                            st.markdown("---")
                    else:
                        st.info("No files uploaded yet.")
                else:
                    st.error("❌ DOB does not match")
            else:
                st.error("❌ Citizen not found")
        except Exception as e:
            st.error(f"❌ Error: {e}")
