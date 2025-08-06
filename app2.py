import streamlit as st
import mysql.connector
from datetime import datetime

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",         # Or public host if deploying
    user="root",              # Change if different
    password="anurag", # Replace with your actual password
    database="assets_db"
)
cursor = conn.cursor()

st.title("Office Assets Information Form")

# Form UI
with st.form("assets_form"):
    asset_type = st.selectbox("Asset Type", ["Laptop", "Mouse", "Extension Box", "TV", "Monitor", "Keyboard", "Projector"])
    serial_number = st.text_input("Serial Number")
    branch = st.text_input("Branch (e.g., Kalyan Nagar, Bangalore)")
    purchase_year = st.number_input("Year of Purchase", min_value=2000, max_value=2099, step=1)
    condition = st.selectbox("Condition", ["Good", "Needs Repair", "Bad"])
    remarks = st.text_area("Remarks (optional)")
    submitted = st.form_submit_button("Submit")

# Insert into DB
if submitted:
    try:
        cursor.execute("""
            INSERT INTO assets (asset_type, serial_number, branch, purchase_year, asset_condition, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (asset_type, serial_number, branch, purchase_year, condition, remarks))
        conn.commit()
        st.success("Form submitted and saved to database!")
    except Exception as e:
        st.error(f"Error: {e}")
