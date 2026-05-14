import pandas as pd
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Healthcare Device Monitor",
    page_icon="🩺",
    layout="wide",
)

st.title("Healthcare Device Monitoring Dashboard")
st.caption("Simulated device health monitoring dashboard for portfolio/demo use.")


def fetch_json(endpoint: str):
    response = requests.get(f"{API_URL}{endpoint}", timeout=10)
    response.raise_for_status()
    return response.json()


def simulate_data():
    response = requests.post(f"{API_URL}/devices/simulate", timeout=10)
    response.raise_for_status()
    return response.json()


try:
    if st.button("Refresh Simulated Device Data"):
        simulate_data()
        st.success("Device telemetry refreshed successfully.")

    devices = fetch_json("/devices")
    alerts = fetch_json("/alerts")

    devices_df = pd.DataFrame(devices)
    alerts_df = pd.DataFrame(alerts)

    total_devices = len(devices_df)
    online_count = len(devices_df[devices_df["status"] == "Online"])
    warning_count = len(devices_df[devices_df["status"] == "Warning"])
    offline_count = len(devices_df[devices_df["status"] == "Offline"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Devices", total_devices)
    col2.metric("Online", online_count)
    col3.metric("Warning", warning_count)
    col4.metric("Offline", offline_count)

    st.subheader("Device Inventory")
    st.dataframe(devices_df, use_container_width=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Battery Level by Device")
        st.bar_chart(devices_df.set_index("device_id")["battery_level"])

    with chart_col2:
        st.subheader("Signal Strength by Device")
        st.bar_chart(devices_df.set_index("device_id")["signal_strength"])

    st.subheader("Alerts")
    if alerts_df.empty:
        st.success("No active alerts.")
    else:
        st.dataframe(alerts_df, use_container_width=True)

    st.subheader("Download Device Report")
    csv_data = devices_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="device_health_report.csv",
        mime="text/csv",
    )

except requests.exceptions.ConnectionError:
    st.error("API is not running. Start backend using: uvicorn app.main:app --reload")
except Exception as error:
    st.error(f"Something went wrong: {error}")
