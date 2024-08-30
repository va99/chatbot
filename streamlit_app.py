import streamlit as st
import altair as alt
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Referral Patient Tracker",
    page_icon=":hospital:",  # This is an emoji shortcode. Could be a URL too.
)

# Mock Data for Referrals
data = [
    {"id": 1, "referral_id": "R001", "patient_name": "John Doe", "patient_age": 45, "patient_mobile": "9876543210", "tpa_partner": "TPA1"},
    {"id": 2, "referral_id": "R002", "patient_name": "Jane Smith", "patient_age": 34, "patient_mobile": "8765432109", "tpa_partner": "TPA2"},
    {"id": 3, "referral_id": "R003", "patient_name": "Alice Brown", "patient_age": 29, "patient_mobile": "7654321098", "tpa_partner": "TPA3"},
    {"id": 4, "referral_id": "R004", "patient_name": "Bob Johnson", "patient_age": 52, "patient_mobile": "6543210987", "tpa_partner": "TPA1"},
    {"id": 5, "referral_id": "R005", "patient_name": "Carol White", "patient_age": 41, "patient_mobile": "5432109876", "tpa_partner": "TPA2"}
]

# Convert mock data to DataFrame
df = pd.DataFrame(data)

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

# Placeholder data for bed occupancy
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

tpa_data = df['tpa_partner'].value_counts().reset_index()
tpa_data.columns = ['TPA Partner', 'Count']

st.subheader("Best-Selling TPAs")

st.altair_chart(
    alt.Chart(tpa_data)
    .mark_bar()
    .encode(
        x=alt.X('Count', title='Number of Referrals'),
        y=alt.Y('TPA Partner:N', title='TPA Partner')  # Fixed line
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