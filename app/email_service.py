import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
import logging

logger = logging.getLogger(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your-app-password")


def send_alert_email(recipient_email: str, device_id: str, alert: dict) -> bool:
    """Send an alert email to a user"""
    
    try:
        # Create email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = f"🚨 Device Alert: {device_id} - {alert.get('severity', 'Unknown')} Severity"
        
        # Email body
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #d32f2f;">Device Alert Notification</h2>
                <p><strong>Device ID:</strong> {device_id}</p>
                <p><strong>Alert Type:</strong> {alert.get('alert_type', 'Unknown')}</p>
                <p><strong>Severity:</strong> <span style="color: {get_severity_color(alert.get('severity'))};"><strong>{alert.get('severity', 'Unknown')}</strong></span></p>
                <p><strong>Message:</strong> {alert.get('message', 'No message')}</p>
                {f'<p><strong>AI Summary:</strong> {alert.get("ai_summary", "")}</p>' if alert.get('ai_summary') else ''}
                <p style="color: #666; font-size: 12px; margin-top: 20px;">
                    This is an automated alert from the Medical Device Monitor system.
                </p>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Alert email sent to {recipient_email} for device {device_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert email: {str(e)}")
        return False


def send_daily_summary_email(recipient_email: str, summary_data: dict) -> bool:
    """Send daily summary email"""
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "📊 Daily Device Health Summary"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Daily Device Health Summary</h2>
                <table style="border-collapse: collapse; width: 100%;">
                    <tr style="background-color: #1f4788; color: white;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Metric</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Count</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">Total Devices</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{summary_data.get('total_devices', 0)}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">Online</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{summary_data.get('online_count', 0)}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">Warning</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{summary_data.get('warning_count', 0)}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">Offline</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{summary_data.get('offline_count', 0)}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">Active Alerts</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{summary_data.get('alert_count', 0)}</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Daily summary email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send daily summary email: {str(e)}")
        return False


def get_severity_color(severity: str) -> str:
    """Get color based on severity level"""
    colors = {
        'Critical': '#d32f2f',  # Red
        'High': '#f57c00',      # Orange
        'Medium': '#fbc02d',    # Yellow
        'Low': '#388e3c'        # Green
    }
    return colors.get(severity, '#666')
