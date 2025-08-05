import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --------------------------
# Database Setup
# --------------------------
conn = sqlite3.connect("assets.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    asset_type TEXT,
    quantity INTEGER,
    serial_number TEXT,
    branch TEXT,
    condition TEXT,
    remarks TEXT
)
""")
conn.commit()

# --------------------------
# Streamlit UI (Instant Mode)
# --------------------------
st.set_page_config(page_title="Branch Asset Form", layout="centered")
st.title("🏢 Learnmore Technologies Assets Detail Form")

# Common fields
branch = st.text_input("Branch Name* (e.g., Kalyan Nagar, Bangalore)")
remarks = st.text_area("General Remarks (Optional)")

st.markdown("---")

asset_types = ["Laptop", "Mouse", "Monitor", "Keyboard", "Extension Board", "TV", "Phone"]

form_data = []

st.subheader("📋 Select and Fill Asset Details")

for asset in asset_types:
    if st.checkbox(f"{asset}", key=f"check_{asset}"):
        st.markdown(f"**{asset} Details**")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            qty = st.number_input(f"Qty ({asset})", min_value=0, step=1, key=f"qty_{asset}")
        with col2:
            cond = st.selectbox(f"Condition ({asset})", ["", "Good", "Needs Repair", "Bad"], key=f"cond_{asset}")
        with col3:
            serial = ""
            if asset == "Laptop":
                serial = st.text_input("Laptop Serial Number*", key=f"serial_{asset}")

        form_data.append({
            "asset_type": asset,
            "quantity": qty,
            "condition": cond,
            "serial_number": serial
        })

# --------------------------
# Submit Button Outside Form
# --------------------------
if st.button("Submit"):
    if not branch:
        st.error("❌ Please enter branch name.")
    elif not form_data:
        st.error("⚠️ Please select and fill at least one asset.")
    elif any(asset["asset_type"] == "Laptop" and not asset["serial_number"] for asset in form_data):
        st.error("❌ Laptop serial number is required.")
    elif any(asset["condition"] == "" for asset in form_data):
        st.error("❌ Please select condition for all selected assets.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for asset in form_data:
            cursor.execute("""
                INSERT INTO assets (timestamp, asset_type, quantity, serial_number, branch, condition, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                asset["asset_type"],
                asset["quantity"],
                asset["serial_number"],
                branch,
                asset["condition"],
                remarks
            ))
        conn.commit()
        st.success("✅ Asset details submitted successfully!")

# --------------------------
# View Submitted Data
# --------------------------
st.markdown("## 📊 View Submitted Data")

if st.checkbox("Show all submissions"):
    df = pd.read_sql_query("SELECT * FROM assets ORDER BY id DESC", conn)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name='submitted_assets.csv', mime='text/csv')
