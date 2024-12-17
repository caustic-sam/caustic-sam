import streamlit as st
import pandas as pd
import os

# Adjust this path if needed
DOWNLOAD_DIR = os.path.expanduser("~/Documents/nist_downloads_http2")
EXCEL_FILE = os.path.join(DOWNLOAD_DIR, "download_log.xlsx")

# Set the page layout to wide for better viewing
st.set_page_config(layout="wide")

st.title("NIST Download Log Viewer")

def make_clickable(title, base_url, filename):
    """Generates a Markdown-formatted clickable link."""
    url = f"{base_url}/{filename}"
    return f"[{title}]({url})"

if os.path.exists(EXCEL_FILE):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(EXCEL_FILE, sheet_name="Download Log")

    # Assume URLs follow a base URL pattern
    BASE_URL = "https://nvlpubs.nist.gov/nistpubs"  # Adjust as necessary

    st.write(f"**Displaying {len(df)} logs with clickable document links:**")

    # Build and display rows manually
    for _, row in df.iterrows():
        title = row["Title"]
        url = f"{BASE_URL}/{title}.pdf"
        st.markdown(f"- [{title}]({url})", unsafe_allow_html=True)

else:
    st.error(f"Log file not found at: {EXCEL_FILE}")