import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

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

# Display metrics at the top
st.markdown(
    f"""
    ### **Total Patients: {total_patients}**
    **Revenue (INR): ₹{total_revenue_inr:,.2f}**
    """,
    unsafe_allow_html=True
)

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