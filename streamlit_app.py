import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Referral Patient Tracker",
    page_icon=":hospital:",  # This is an emoji shortcode. Could be a URL too.
)

# Mock Data for Referrals in India
data = [
    {"id": 1, "referral_id": "R001", "patient_name": "Amit Sharma", "patient_age": 45, "patient_mobile": "9876543210", "mode_of_payment": "TPA", "tpa_partner": "TPA1", "city": "Mumbai"},
    {"id": 2, "referral_id": "R002", "patient_name": "Anita Singh", "patient_age": 34, "patient_mobile": "8765432109", "mode_of_payment": "Cash", "tpa_partner": None, "city": "Delhi"},
    {"id": 3, "referral_id": "R003", "patient_name": "Raj Patel", "patient_age": 29, "patient_mobile": "7654321098", "mode_of_payment": "TPA", "tpa_partner": "TPA3", "city": "Bengaluru"},
    {"id": 4, "referral_id": "R004", "patient_name": "Sita Gupta", "patient_age": 52, "patient_mobile": "6543210987", "mode_of_payment": "TPA", "tpa_partner": "TPA1", "city": "Mumbai"},
    {"id": 5, "referral_id": "R005", "patient_name": "Ravi Kumar", "patient_age": 41, "patient_mobile": "5432109876", "mode_of_payment": "Cash", "tpa_partner": None, "city": "Delhi"}
]

# Convert mock data to DataFrame
df = pd.DataFrame(data)

# Calculate total patients and revenue
total_patients = len(df)
revenue_per_patient = 1299  # USD
total_revenue = total_patients * revenue_per_patient

# Generate random times saved data
np.random.seed(0)  # For reproducibility
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

# Display Total Patients and Revenue
st.write(f"**Total Patients**: {total_patients}")
st.write(f"**Revenue**: ₹{total_revenue * 82.3:,.2f}")  # Converting USD to INR (1 USD = 82.3 INR approximately)

# Visualization: Bed Occupancy

# Placeholder data for bed occupancy in India
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

# Extract only TPA entries for this visualization
tpa_df = df[df['mode_of_payment'] == 'TPA']
tpa_data = tpa_df['tpa_partner'].value_counts().reset_index()
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