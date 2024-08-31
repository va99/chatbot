import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set up the page title and icon
st.set_page_config(page_title="Hospital Admin Dashboard", page_icon="🏥")

# Mock TPA data
tpa_data = {
    "01": "Medi Assist", "02": "Paramount Health Services", "03": "FHPL",
    "04": "Health India TPA", "05": "Star Health", "06": "Apollo Munich",
    "07": "ICICI Lombard", "08": "UnitedHealthcare", "09": "Religare Health Insurance",
    "10": "HDFC ERGO", "11": "Max Bupa", "12": "SBI Health Insurance", "13": "New India Assurance",
    "14": "Oriental Insurance", "15": "National Insurance", "16": "United India Insurance",
    "17": "IFFCO Tokio", "18": "Cholamandalam MS", "19": "Bajaj Allianz", "20": "Reliance General Insurance"
}

# Generate mock data for patients and TPAs
np.random.seed(42)
cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"]
modes = ["TPA", "Cash"]
data = [{
    "id": i + 1, "referral_id": f"R{str(i + 1).zfill(3)}", "patient_name": f"Patient {i + 1}",
    "patient_age": np.random.randint(20, 80), "patient_mobile": f"9{np.random.randint(100000000, 999999999)}",
    "mode_of_payment": np.random.choice(modes), "tpa_partner": np.random.choice(list(tpa_data.keys())) if np.random.choice(modes) == "TPA" else None,
    "city": np.random.choice(cities)
} for i in range(100)]

df = pd.DataFrame(data)
df['tpa_partner_name'] = df['tpa_partner'].map(tpa_data).fillna('N/A')

# Metrics
total_patients = len(df)
total_revenue_inr = total_patients * 1299 * 82.3
cash_patients = df['mode_of_payment'].value_counts().get('Cash', 0)
tpa_patients = df['mode_of_payment'].value_counts().get('TPA', 0)

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Patients", total_patients)
with col2: st.metric("Revenue (INR)", f"₹{total_revenue_inr:,.2f}")
with col3: st.metric("Cash Patients", cash_patients)
with col4: st.metric("TPA Patients", tpa_patients)

# TPA Partner Distribution
st.subheader("TPA Partner Distribution")
tpa_distribution = df['tpa_partner_name'].value_counts().reset_index()
tpa_distribution.columns = ['TPA Partner', 'Count']
chart_tpa = alt.Chart(tpa_distribution).mark_bar().encode(
    x=alt.X('Count:Q', title='Number of Patients'),
    y=alt.Y('TPA Partner:N', sort='-x', title='TPA Partner')
).properties(width=700)
st.altair_chart(chart_tpa)

# Bed Occupancy Data
st.subheader("Bed Occupancy")
bed_occupancy_data = pd.DataFrame({
    'Unit': ['ICU', 'General Ward', 'Emergency', 'Maternity', 'Pediatrics'],
    'Occupied': [10, 30, 5, 8, 15],
    'Total': [15, 50, 10, 12, 20]
})
bed_occupancy_data['Available'] = bed_occupancy_data['Total'] - bed_occupancy_data['Occupied']
chart_bed = alt.Chart(bed_occupancy_data).mark_bar().encode(
    x=alt.X('Available:Q', title='Available Beds'),
    y=alt.Y('Unit:N', sort='-x', title='Unit')
).properties(width=700)
st.altair_chart(chart_bed)

# Top Regions
st.subheader("Top Regions")
region_data = df['city'].value_counts().reset_index()
region_data.columns = ['City', 'Number of Referrals']
chart_region = alt.Chart(region_data).mark_bar().encode(
    x=alt.X('Number of Referrals:Q', title='Number of Referrals'),
    y=alt.Y('City:N', sort='-x', title='City')
).properties(width=700)
st.altair_chart(chart_region)

# Display the DataFrame for detailed view
st.subheader("Detailed Data View")
st.dataframe(df)

# Optionally download the data
st.download_button(
    label="Download Data as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='hospital_admin_data.csv',
    mime='text/csv'
)