import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Set up the page title and icon
st.set_page_config(page_title="Referral Patient Tracker", page_icon=":hospital:")

# Mock data
tpa_data = {
    "01": "Medi Assist", "02": "Paramount Health Services", "03": "FHPL",
    "04": "Health India TPA", "05": "Star Health", "06": "Apollo Munich",
    "07": "ICICI Lombard", "08": "UnitedHealthcare", "09": "Religare Health Insurance",
    "10": "HDFC ERGO", "11": "Max Bupa", "12": "SBI Health Insurance", "13": "New India Assurance",
    "14": "Oriental Insurance", "15": "National Insurance", "16": "United India Insurance",
    "17": "IFFCO Tokio", "18": "Cholamandalam MS", "19": "Bajaj Allianz", "20": "Reliance General Insurance"
}

# Generate mock data
np.random.seed(0)
cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"]
modes = ["TPA", "Cash"]
data = [{
    "id": i + 1, "referral_id": f"R{str(i + 1).zfill(3)}", "patient_name": f"Patient {i + 1}",
    "patient_age": np.random.randint(20, 80), "patient_mobile": f"9{np.random.randint(100000000, 999999999)}",
    "mode_of_payment": np.random.choice(modes), "tpa_partner": np.random.choice(list(tpa_data.keys())) if np.random.choice(modes) == "TPA" else None,
    "city": np.random.choice(cities)
} for i in range(67)]

df = pd.DataFrame(data)
df['tpa_partner_name'] = df['tpa_partner'].map(tpa_data).fillna('N/A')

# Metrics
total_patients = len(df)
total_revenue_inr = total_patients * 1299 * 82.3
cash_patients = df['mode_of_payment'].value_counts().get('Cash', 0)
tpa_patients = df['mode_of_payment'].value_counts().get('TPA', 0)
total_hours_saved = df['time_saved_minutes'].sum() / 60

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Patients", total_patients)
with col2: st.metric("Revenue (INR)", f"₹{total_revenue_inr:,.2f}")
with col3: st.metric("Cash Patients", cash_patients)
with col4: st.metric("TPA Patients", tpa_patients)

# Visualizations
visualizations = {
    "Bed Occupancy": {
        'Unit': ['ICU', 'General Ward', 'Emergency', 'Maternity', 'Pediatrics'],
        'Occupied': [10, 30, 5, 8, 15],
        'Total': [15, 50, 10, 12, 20]
    },
    "Best-Selling TPAs": df[df['mode_of_payment'] == 'TPA']['tpa_partner_name'].value_counts().reset_index(),
    "Top Regions": df['city'].value_counts().reset_index()
}

for title, data in visualizations.items():
    st.subheader(title)
    chart_data = pd.DataFrame(data)
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Count' if 'Count' in chart_data.columns else 'Available', title='Count'),
        y=alt.Y('index', title='Category'),
        color='index' if 'index' in chart_data.columns else None
    ).properties(title=title).interactive()
    st.altair_chart(chart, use_container_width=True)

# Pre-auth form
st.title("Pre-Authorization Manager")
selected_referral_id = st.selectbox("Select Referral ID", df['referral_id'])
selected_referral = df[df['referral_id'] == selected_referral_id].iloc[0]

with st.form(key='pre_auth_form'):
    st.subheader("Patient Information")
    patient_name = st.text_input("Name", value=selected_referral["patient_name"])
    patient_age = st.number_input("Age", value=selected_referral["patient_age"])
    patient_gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    patient_contact = st.text_input("Contact Number", value=selected_referral["patient_mobile"])

    st.subheader("Insurance Details")
    insurance_provider = st.text_input("Insurance Provider", value=selected_referral["tpa_partner_name"])
    policy_number = st.text_input("Policy Number", "Sample Policy Number")
    coverage_details = st.text_input("Coverage Details", "Sample Coverage Details")

    st.subheader("Medical History")
    requested_treatment = st.text_input("Requested Treatment", "Sample Treatment")
    diagnosis = st.text_input("Diagnosis", "Sample Diagnosis")
    proposed_date = st.date_input("Proposed Date", pd.to_datetime("2024-09-15"))
    previous_treatments = st.text_area("Previous Treatments", "Sample Previous Treatments")
    current_medications = st.text_area("Current Medications", "Sample Current Medications")
    allergies = st.text_area("Allergies", "Sample Allergies")

    st.subheader("Provider Information")
    hospital_name = st.text_input("Hospital/Clinic Name", "Sample Hospital")
    doctor_name = st.text_input("Doctor's Name", "Sample Doctor")

    st.subheader("Authorization Request Details")
    request_date = st.date_input("Date of Request", pd.to_datetime("2024-08-30"))

    if st.form_submit_button("Submit"):
        st.success("Pre-Authorization Request Submitted Successfully!")
        st.write({
            "Name": patient_name, "Age": patient_age, "Gender": patient_gender, "Contact": patient_contact,
            "Insurance Provider": insurance_provider, "Policy Number": policy_number, "Coverage Details": coverage_details,
            "Requested Treatment": requested_treatment, "Diagnosis": diagnosis, "Proposed Date": proposed_date,
            "Previous Treatments": previous_treatments, "Current Medications": current_medications, "Allergies": allergies,
            "Hospital/Clinic Name": hospital_name, "Doctor's Name": doctor_name, "Date of Request": request_date
        })