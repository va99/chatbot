import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Referral Patient Tracker",
    page_icon=":hospital:",  # This is an emoji shortcode. Could be a URL too.
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

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    key="referrals_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.referrals_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Normally would update data in the database, but now it's just for the UI.
)

# Create a layout with columns for metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Patients", value=total_patients)

with col2:
    st.metric(label="Revenue (INR)", value=f"₹{total_revenue_inr:,.2f}")

# Pre-Auth Manager Section
st.subheader("Pre-Authorization Manager")

# Create a form for entering patient details
with st.form(key='pre_auth_form'):
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Patient Age", min_value=0, max_value=120)
    treatment = st.selectbox("Treatment", ["Surgery", "Consultation", "Medication"])
    submission_date = st.date_input("Submission Date")
    
    # Simulated ML model for prediction (e.g., predicting the status of the pre-auth request)
    if st.form_submit_button("Predict and Submit"):
        # Simulate ML prediction
        st.write(f"Patient Name: {patient_name}")
        st.write(f"Patient Age: {patient_age}")
        st.write(f"Treatment: {treatment}")
        st.write(f"Submission Date: {submission_date}")
        
        # Simulated machine learning prediction (e.g., treatment classification)
        # Here, we just use random selection for simulation
        statuses = ["Pending", "Approved", "Rejected"]
        status = np.random.choice(statuses)
        
        st.write(f"Predicted Status: {status}")
        
        # In a real application, here you would process the submission
        st.success("Pre-authorization request has been submitted!")

# Visualization: Bed Occupancy
st.subheader("Bed Occupancy")

# Placeholder data for bed occupancy in India
bed_occupancy_data = pd.DataFrame({
    'Unit': ['ICU', 'General Ward', 'Emergency', 'Maternity', 'Pediatrics'],
    'Occupied': [10, 30, 5, 8, 15],
    'Total': [15, 50, 10, 12, 20]
})

bed_occupancy_data['Available'] = bed_occupancy_data['Total'] - bed_occupancy_data['Occupied']

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
st.subheader("Best-Selling TPAs")

# Extract only TPA entries for this visualization
tpa_df = df[df['mode_of_payment'] == 'TPA']
tpa_data = tpa_df['tpa_partner_name'].value_counts().reset_index()
tpa_data.columns = ['TPA Partner', 'Count']

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
st.subheader("Top Regions for You")

region_data = df['city'].value_counts().reset_index()
region_data.columns = ['City', 'Number of Referrals']

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