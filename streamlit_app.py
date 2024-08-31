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

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Patients", total_patients)
with col2: st.metric("Revenue (INR)", f"₹{total_revenue_inr:,.2f}")
with col3: st.metric("Cash Patients", cash_patients)
with col4: st.metric("TPA Patients", tpa_patients)

# Visualizations
def plot_chart(data, x_col, y_col, color_col=None):
    if not data.empty and x_col in data.columns and y_col in data.columns:
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(x_col, title='Count'),
            y=alt.Y(y_col, title='Category'),
            color=color_col
        ).properties(title=y_col).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning(f"Insufficient or incorrect data for plotting: {y_col}")

# Bed Occupancy
bed_occupancy_data = pd.DataFrame({
    'Unit': ['ICU', 'General Ward', 'Emergency', 'Maternity', 'Pediatrics'],
    'Occupied': [10, 30, 5, 8, 15],
    'Total': [15, 50, 10, 12, 20]
})
bed_occupancy_data['Available'] = bed_occupancy_data['Total'] - bed_occupancy_data['Occupied']
st.subheader("Bed Occupancy")
plot_chart(bed_occupancy_data, 'Available', 'Unit', 'Unit')

# Best-Selling TPAs
tpa_df = df[df['mode_of_payment'] == 'TPA']['tpa_partner_name'].value_counts().reset_index()
tpa_df.columns = ['TPA Partner', 'Count']
st.subheader("Best-Selling TPAs")
plot_chart(tpa_df, 'Count', 'TPA Partner')

# Top Regions
region_data = df['city'].value_counts().reset_index()
region_data.columns = ['City', 'Number of Referrals']
st.subheader("Top Regions for You")
plot_chart(region_data, 'Number of Referrals', 'City', 'City')