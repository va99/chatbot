import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Set up the page title and icon
st.set_page_config(
    page_title="Referral Patient Tracker",
    page_icon=":hospital:"
)

# TPA mock data
tpa_data = {
    "01": "Medi Assist",
    "02": "Paramount Health Services",
    "03": "FHPL (Family Health Plan Limited)",
    "04": "Health India TPA",
    "05": "Star Health",
    "06": "Apollo Munich",
    "07": "ICICI Lombard",
    "08": "UnitedHealthcare",
    "09": "Religare Health Insurance",
    "10": "HDFC ERGO",
    "11": "Max Bupa Health Insurance",
    "12": "SBI Health Insurance",
    "13": "New India Assurance",
    "14": "Oriental Insurance",
    "15": "National Insurance",
    "16": "United India Insurance",
    "17": "IFFCO Tokio",
    "18": "Cholamandalam MS General Insurance",
    "19": "Bajaj Allianz",
    "20": "Reliance General Insurance"
}

# Generate mock data for 67 referrals
np.random.seed(0)  # For reproducibility
cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"]
modes_of_payment = ["TPA", "Cash"]
tpas = list(tpa_data.keys())

data = []
for i in range(67):
    mode = np.random.choice(modes_of_payment)
    tpa_partner = np.random.choice(tpas) if mode == "TPA" else None
    data.append({
        "id": i + 1,
        "referral_id": f"R{str(i + 1).zfill(3)}",
        "patient_name": f"Patient {i + 1}",
        "patient_age": np.random.randint(20, 80),
        "patient_mobile": f"9{np.random.randint(100000000, 999999999)}",
        "mode_of_payment": mode,
        "tpa_partner": tpa_partner,
        "city": np.random.choice(cities)
    })

# Convert mock data to DataFrame
df = pd.DataFrame(data)

# Map TPA codes to TPA names
df['tpa_partner_name'] = df['tpa_partner'].map(tpa_data).fillna('N/A')

# Calculate total patients and revenue
total_patients = len(df)
revenue_per_patient = 1299  # USD
total_revenue_usd = total_patients * revenue_per_patient
total_revenue_inr = total_revenue_usd * 82.3  # Convert USD to INR (1 USD ≈ 82.3 INR)

# Calculate count of Cash and TPA patients
cash_patients = df[df['mode_of_payment'] == 'Cash'].shape[0]
tpa_patients = df[df['mode_of_payment'] == 'TPA'].shape[0]

# Generate random times saved data
df['time_saved_minutes'] = np.random.randint(5, 15, size=len(df))  # Random minutes saved between 5 and 15

# Calculate total hours saved
total_minutes_saved = df['time_saved_minutes'].sum()
total_hours_saved = total_minutes_saved / 60

# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Patients", value=total_patients)

with col2:
    st.metric(label="Revenue (INR)", value=f"₹{total_revenue_inr:,.2f}")

with col3:
    st.metric(label="Cash Patients", value=cash_patients)

with col4:
    st.metric(label="TPA Patients", value=tpa_patients)

# Visualization: Bed Occupancy
bed_occupancy_data = pd.DataFrame({
    'Unit': ['ICU', 'General Ward', 'Emergency', 'Maternity', 'Pediatrics'],
    'Occupied': [10, 30, 5, 8, 15],
    'Total': [15, 50, 10, 12, 20]
})

bed_occupancy_data['Available'] = bed_occupancy_data['Total'] - bed_occupancy_data['Occupied']

st.subheader("Bed Occupancy")

st.altair_chart(
    alt.Chart(bed_occupancy_data)
    .mark_bar()
    .encode(
        x=alt.X('Unit', title='Unit'),
        y=alt.Y('Available', title='Available Beds'),
        color='Unit'
    )
    .properties(
        title="Bed Occupancy"
    )
    .interactive()
    .configure_axis(
        labelAngle=0
    ),
    use_container_width=True
)

# Visualization: Best-Selling TPAs
tpa_df = df[df['mode_of_payment'] == 'TPA']
tpa_data = tpa_df['tpa_partner_name'].value_counts().reset_index()
tpa_data.columns = ['TPA Partner', 'Count']

st.subheader("Best-Selling TPAs")

st.altair_chart(
    alt.Chart(tpa_data)
    .mark_bar()
    .encode(
        x=alt.X('Count', title='Number of Referrals'),
        y=alt.Y('TPA Partner:N', title='TPA Partner')
    )
    .properties(
        title="Best-Selling TPAs"
    )
    .interactive()
    .configure_axis(
        labelAngle=0
    ),
    use_container_width=True
)

# Visualization: Top Regions for You
region_data = df['city'].value_counts().reset_index()
region_data.columns = ['City', 'Number of Referrals']

st.subheader("Top Regions for You")

st.altair_chart(
    alt.Chart(region_data)
    .mark_bar()
    .encode(
        x=alt.X('Number of Referrals', title='Number of Referrals'),
        y=alt.Y('City:N', title='City'),
        color='City'
    )
    .properties(
        title="Top Regions for You"
    )
    .interactive()
    .configure_axis(
        labelAngle=0
    ),
    use_container_width=True
)

# Pre-auth form
st.title("Pre-Authorization Manager")

# Create a dropdown to select a referral for the pre-auth form
selected_referral_id = st.selectbox("Select Referral ID", df['referral_id'].tolist())

# Filter data for the selected referral
selected_referral = df[df['referral_id'] == selected_referral_id].iloc[0]

# Pre-auth form
with st.form(key='pre_auth_form'):
    st.subheader("Patient Information")
    patient_name = st.text_input("Name", value=selected_referral["patient_name"])
    patient_age = st.number_input("Age", value=selected_referral["patient_age"])
    patient_gender = st.selectbox("Gender", ["Male", "Female"], index=0)  # Assuming gender is not in the data, default to "Male"
    patient_contact = st.text_input("Contact Number", value=selected_referral["patient_mobile"])

    st.subheader("Insurance Details")
    insurance_provider = st.text_input("Insurance Provider", value=selected_referral["tpa_partner_name"])
    policy_number = st.text_input("Policy Number", "Sample Policy Number")  # Placeholder, update as needed
    coverage_details = st.text_input("Coverage Details", "Sample Coverage Details")  # Placeholder, update as needed

    st.subheader("Medical History")
    requested_treatment = st.text_input("Requested Treatment", "Sample Treatment")  # Placeholder, update as needed
    diagnosis = st.text_input("Diagnosis", "Sample Diagnosis")  # Placeholder, update as needed
    proposed_date = st.date_input("Proposed Date", pd.to_datetime("2024-09-15"))

    previous_treatments = st.text_area("Previous Treatments", "Sample Previous Treatments")  # Placeholder, update as needed
    current_medications = st.text_area("Current Medications", "Sample Current Medications")  # Placeholder, update as needed
    allergies = st.text_area("Allergies", "Sample Allergies")  # Placeholder, update as needed

    st.subheader("Provider Information")
    hospital_name = st.text_input("Hospital/Clinic Name", "Sample Hospital")  # Placeholder, update as needed
    doctor_name = st.text_input("Doctor's Name", "Sample Doctor")  # Placeholder, update as needed

    st.subheader("Authorization Request Details")
    request_date = st.date_input("Date of Request", pd.to_datetime("2024-08-30"))

    # Submit button
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.success("Pre-Authorization Request Submitted Successfully!")
        # Display submitted data
        st.write("Form Data:")
        st.write({
            "Name": patient_name,
            "Age": patient_age,
            "Gender": patient_gender,
            "Contact": patient_contact,
            "Insurance Provider": insurance_provider,
            "Policy Number": policy_number,
            "Coverage Details": coverage_details,
            "Requested Treatment": requested_treatment,
            "Diagnosis": diagnosis,
            "Proposed Date": proposed_date,
            "Previous Treatments": previous_treatments,
            "Current Medications": current_medications,
            "Allergies": allergies,
            "Hospital Name": hospital_name,
            ""Doctor's Name": doctor_name,
            "Request Date": request_date
        })