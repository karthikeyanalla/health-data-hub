import streamlit as st
import requests

BASE_URL = "http://localhost:5001/api"

def main():
    if "role" not in st.session_state:
        st.session_state.role = None
    if "token" not in st.session_state:
        st.session_state.token = None

    def login_page():
        st.title("🏥 Hospital Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["token"]
                st.session_state.role = "hospital"
                st.success("✅ Logged in successfully.")
            else:
                st.error("❌ Login failed.")

    def dashboard():
        st.title("🏥 Hospital Dashboard")
        menu = st.sidebar.radio("Select an option", ["Add Citizen", "Upload File", "View Citizen"])
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        if menu == "Add Citizen":
            st.subheader("Add New Citizen")
            name = st.text_input("Name")
            id_number = st.text_input("ID Number")
            dob = st.date_input("Date of Birth")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=0)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            bloodType = st.text_input("Blood Type")
            allergies = st.text_area("Allergies")
            medications = st.text_area("Medications")

            if st.button("Submit"):
                payload = {
                    "name": name,
                    "idNumber": id_number,
                    "dob": dob.isoformat(),
                    "phone": phone,
                    "email": email,
                    "age": age,
                    "gender": gender,
                    "bloodType": bloodType,
                    "allergies": allergies,
                    "medications": medications
                }
                try:
                    r = requests.post(
                        f"{BASE_URL}/citizens",
                        headers={"Authorization": f"Bearer {st.session_state.token}", "Content-Type": "application/json"},
                        json=payload
                    )
                    if r.status_code == 201:
                        st.success("✅ Citizen added!")
                    else:
                        st.error(f"❌ Failed: {r.status_code} — {r.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        elif menu == "Upload File":
            st.subheader("Upload Medical File")
            citizen_id = st.text_input("Citizen ID")
            file = st.file_uploader("Upload file")

            if file and st.button("Upload"):
                try:
                    files = {"file": (file.name, file, file.type)}
                    r = requests.post(
                        f"{BASE_URL}/upload?citizenId={citizen_id}",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        files=files
                    )
                    if r.status_code in [200, 201]:
                        st.success("✅ File uploaded successfully")
                    else:
                        st.error(f"❌ Upload failed: {r.status_code} — {r.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        elif menu == "View Citizen":
            st.subheader("View Citizen Details")
            citizen_id = st.text_input("Enter Citizen ID")
            if st.button("Search"):
                try:
                    r = requests.get(
                        f"{BASE_URL}/citizens/idNumber/{citizen_id}",
                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    if r.status_code == 200:
                        citizen = r.json()
                        st.write(f"👤 Name: {citizen['name']}")
                        st.write(f"📧 Email: {citizen['email']}")
                        st.write(f"📞 Phone: {citizen['phone']}")
                        st.write(f"🤧 Allergies: {citizen.get('allergies', 'N/A')}")
                        st.write(f"🩺 Blood Type: {citizen.get('bloodType', 'N/A')}")
                        st.write(f"💊 Medications: {citizen.get('medications', 'N/A')}")
                        st.write(f"📂 Files uploaded: {len(citizen['uploadedFiles'])}")
                        
                        if citizen["uploadedFiles"]:
                            st.markdown("### 📄 Uploaded Files")
                            for file in citizen["uploadedFiles"]:
                                file_name = file.get("fileName", "Unnamed")
                                file_type = file.get("fileType", "Unknown")
                                file_url = f"{BASE_URL.replace('/api', '')}/uploads/{file['filePath'].split('/')[-1]}"
                                st.write(f"**{file_name}** ({file_type})")
                                st.markdown(f"[📥 Download File]({file_url})", unsafe_allow_html=True)
                                st.markdown("---")
                        else:
                            st.info("ℹ️ No files uploaded for this citizen.")
                    else:
                        st.error(f"❌ Not found: {r.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    if st.session_state.token:
        dashboard()
    else:
        login_page()
