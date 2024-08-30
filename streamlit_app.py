from collections import defaultdict
from pathlib import Path
import sqlite3
import streamlit as st
import altair as alt
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Referral Patient Tracker",
    page_icon=":hospital:"  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def connect_db():
    """Connects to the sqlite database."""
    DB_FILENAME = Path(__file__).parent / "referral_patient_tracker.db"
    db_already_exists = DB_FILENAME.exists()
    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists
    return conn, db_was_just_created

def initialize_data(conn):
    """Initializes the referral patient tracker table with some data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referral_id TEXT,
            patient_name TEXT,
            patient_age INTEGER,
            patient_mobile TEXT,
            tpa_partner TEXT,
            mode_of_payment TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO referrals
            (referral_id, patient_name, patient_age, patient_mobile, tpa_partner, mode_of_payment)
        VALUES
            ('R001', 'John Doe', 45, '9876543210', 'TPA1', 'TPA'),
            ('R002', 'Jane Smith', 34, '8765432109', 'TPA2', 'Cash'),
            ('R003', 'Alice Brown', 29, '7654321098', 'TPA3', 'TPA'),
            ('R004', 'Bob Johnson', 52, '6543210987', 'TPA1', 'Cash'),
            ('R005', 'Carol White', 41, '5432109876', 'TPA2', 'TPA')
        """
    )
    conn.commit()

def load_data(conn):
    """Loads the referral patient data from the database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM referrals")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "referral_id",
            "patient_name",
            "patient_age",
            "patient_mobile",
            "tpa_partner",
            "mode_of_payment"
        ],
    )
    return df

def update_data(conn, df, changes):
    """Updates the referral patient data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.referrals_table["edited_rows"]
        rows = []
        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE referrals
            SET
                referral_id = :referral_id,
                patient_name = :patient_name,
                patient_age = :patient_age,
                patient_mobile = :patient_mobile,
                tpa_partner = :tpa_partner,
                mode_of_payment = :mode_of_payment
            WHERE id = :id
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO referrals
                (id, referral_id, patient_name, patient_age, patient_mobile, tpa_partner, mode_of_payment)
            VALUES
                (:id, :referral_id, :patient_name, :patient_age, :patient_mobile, :tpa_partner, :mode_of_payment)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM referrals WHERE id = :id",
            ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()

# -----------------------------------------------------------------------------
# Define TPA options (Mock Data from Doctor App)
tpa_options = ["TPA1", "TPA2", "TPA3"]

# Home screen content
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")

# Load data from database
df = load_data(conn)

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
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.referrals_table),
)

# -----------------------------------------------------------------------------
# Visualization: TPA Referrals Breakdown

# Transforming the data for visualization
tpa_breakdown = df.groupby(['mode_of_payment', 'tpa_partner']).size().reset_index(name='Count')

st.subheader("TPA Referrals Breakdown")

st.altair_chart(
    alt.Chart(tpa_breakdown)
    .mark_bar()
    .encode(
        x=alt.X('Count', title='Number of Referrals'),
        y=alt.Y('tpa_partner:N', title='TPA Partner'),
        color='mode_of_payment:N',
        column='mode_of_payment:N'
    )
    .properties(
        title="Referrals by TPA Partner and Payment Mode"
    )
    .interactive()
    .configure_axis(
        labelAngle=0
    ),
    use_container_width=True
)

# -----------------------------------------------------------------------------
# Visualization: Hours Saved Comparison

# Placeholder data for hours saved
hours_saved_data = pd.DataFrame({
    'Process': ['Manual Form Filling', 'Automated System'],
    'Hours': [20, 5]
})

st.subheader("Hours Saved Comparison")

st.altair_chart(
    alt.Chart(hours_saved_data)
    .mark_bar()
    .encode(
        x=alt.X('Process', title='Process'),
        y=alt.Y('Hours', title='Hours'),
        color='Process'
    )
    .properties(
        title="Comparison of Hours Saved"
    )
    .interactive()
    .configure_axis(
        labelAngle=0
    ),
    use_container_width=True
)