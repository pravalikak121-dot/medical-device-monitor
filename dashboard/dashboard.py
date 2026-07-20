import pandas as pd
import requests
import streamlit as st
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Healthcare Device Monitor",
    page_icon="🩺",
    layout="wide",
)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None


def login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🏥 Healthcare Device Monitor")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                try:
                    response = requests.post(
                        f"{API_URL}/api/v1/auth/login",
                        json={"username": username, "password": password},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
        
        with tab2:
            st.subheader("Register")
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            
            role = st.selectbox(
                "Role",
                ["nurse", "doctor", "admin"],
                key="reg_role"
            )
            
            if st.button("Register", use_container_width=True):
                try:
                    response = requests.post(
                        f"{API_URL}/api/v1/auth/register",
                        json={
                            "username": new_username,
                            "email": new_email,
                            "password": new_password,
                            "role": role
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(response.json().get("detail", "Registration failed"))
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")


def dashboard_page():
    """Display main dashboard"""
    
    # Header with logout
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown("## 🏥 Healthcare Device Monitoring Dashboard")
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
    
    st.markdown("---")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    try:
        # Fetch devices and alerts
        devices_response = requests.get(
            f"{API_URL}/api/v1/devices",
            headers=headers,
            timeout=10
        )
        alerts_response = requests.get(
            f"{API_URL}/api/v1/alerts",
            headers=headers,
            timeout=10
        )
        
        if devices_response.status_code != 200:
            st.error("Failed to fetch devices")
            return
        
        devices = devices_response.json()
        alerts = alerts_response.json() if alerts_response.status_code == 200 else []
        
        # Create DataFrames
        devices_df = pd.DataFrame(devices)
        alerts_df = pd.DataFrame(alerts) if alerts else pd.DataFrame()
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_devices = len(devices_df)
        online_count = len(devices_df[devices_df["status"] == "Online"]) if "status" in devices_df.columns else 0
        warning_count = len(devices_df[devices_df["status"] == "Warning"]) if "status" in devices_df.columns else 0
        offline_count = len(devices_df[devices_df["status"] == "Offline"]) if "status" in devices_df.columns else 0
        
        col1.metric("Total Devices", total_devices)
        col2.metric("Online", online_count, delta="✅")
        col3.metric("Warning", warning_count, delta="⚠️")
        col4.metric("Offline", offline_count, delta="❌")
        
        st.markdown("---")
        
        # Device Inventory
        st.subheader("📱 Device Inventory")
        if not devices_df.empty:
            st.dataframe(devices_df, use_container_width=True, hide_index=True)
        else:
            st.info("No devices assigned")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔋 Battery Level by Device")
            if "device_id" in devices_df.columns and "battery_level" in devices_df.columns:
                battery_data = devices_df.set_index("device_id")["battery_level"]
                st.bar_chart(battery_data)
        
        with col2:
            st.subheader("📡 Signal Strength by Device")
            if "device_id" in devices_df.columns and "signal_strength" in devices_df.columns:
                signal_data = devices_df.set_index("device_id")["signal_strength"]
                st.bar_chart(signal_data)
        
        st.markdown("---")
        
        # Alerts
        st.subheader("🚨 Active Alerts")
        if not alerts_df.empty:
            for idx, alert in alerts_df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Device:** {alert.get('device_id', 'Unknown')}")
                        st.write(f"**Alert Type:** {alert.get('alert_type', 'Unknown')}")
                        st.write(f"**Message:** {alert.get('message', 'No message')}")
                        
                        if alert.get('ai_summary'):
                            st.info(f"**AI Summary:** {alert.get('ai_summary')}")
                    
                    with col2:
                        st.write(f"**{alert.get('severity', 'Unknown')}**")
                        st.caption(f"Created: {alert.get('created_at', 'Unknown')}")
        else:
            st.success("✅ No active alerts")
        
        st.markdown("---")
        
        # Reports section
        st.subheader("📊 Reports")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download Device Report (PDF)"):
                try:
                    response = requests.get(
                        f"{API_URL}/api/v1/reports/devices/pdf",
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        pdf_bytes = bytes.fromhex(data["pdf"])
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=data["filename"],
                            mime=data["content_type"]
                        )
                    else:
                        st.error("Failed to generate report")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("View Alert Summary"):
                try:
                    response = requests.get(
                        f"{API_URL}/api/v1/reports/alerts/summary",
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        summary = response.json()
                        st.json(summary)
                    else:
                        st.error("Failed to fetch summary")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    except requests.exceptions.ConnectionError:
        st.error("🔴 API is not running. Start backend using: uvicorn app.main:app --reload")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


# Main app logic
if st.session_state.token is None:
    login_page()
else:
    dashboard_page()

