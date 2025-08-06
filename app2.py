import streamlit as st
import mysql.connector
from datetime import datetime

# MySQL Connection (update with your password if different)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anurag",  # ← change this
    database="assets_db"
)
cursor = conn.cursor()

# Streamlit Page
st.set_page_config(page_title="Asset Form")
st.title("🏢 Office Assets Information Form")

with st.form("asset_form"):
    asset_type = st.selectbox("Asset Type", [
        "", "Laptop", "Mouse", "Extension Box", "TV", "Monitor", "Keyboard"
    ])
    serial_number = st.text_input("Serial Number")
    branch = st.text_input("Branch", placeholder="e.g., Kalyan Nagar, Bangalore")
    condition = st.selectbox("Condition", ["", "Good", "Needs Repair", "Bad"])
    remarks = st.text_area("Remarks (optional)")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if asset_type and serial_number and branch and condition:
            timestamp = datetime.now()
            cursor.execute("""
                INSERT INTO assets (timestamp, asset_type, quantity, serial_number, branch, asset_condition, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (timestamp, asset_type, 1, serial_number, branch, condition, remarks))
            conn.commit()
            st.success("✅ Asset information submitted!")
        else:
            st.error("Please fill all required fields.")

# View Data
if st.checkbox("Show All Submitted Assets"):
    cursor.execute("SELECT * FROM assets ORDER BY id DESC")
    data = cursor.fetchall()
    col_names = [col[0] for col in cursor.description]

    import pandas as pd
    df = pd.DataFrame(data, columns=col_names)
    st.dataframe(df)
