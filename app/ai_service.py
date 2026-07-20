import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import OpenAI, but allow graceful fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not installed. AI summaries will be disabled.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def generate_alert_summary(alert: dict) -> Optional[str]:
    """Generate AI summary for an alert using OpenAI"""
    
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return generate_rule_based_summary(alert)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""
        You are a medical device monitoring expert. Provide a brief (1-2 sentences) professional summary of the following alert:
        
        Device ID: {alert.get('device_id', 'Unknown')}
        Alert Type: {alert.get('alert_type', 'Unknown')}
        Severity: {alert.get('severity', 'Unknown')}
        Message: {alert.get('message', 'No message')}
        
        Provide practical recommendations for the healthcare staff.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical device monitoring expert providing concise alerts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Failed to generate AI summary: {str(e)}")
        return generate_rule_based_summary(alert)


def generate_rule_based_summary(alert: dict) -> str:
    """Generate summary based on rules (fallback when AI is not available)"""
    
    alert_type = alert.get('alert_type', '').lower()
    severity = alert.get('severity', '').lower()
    battery = alert.get('battery_level', 0) if isinstance(alert.get('battery_level'), int) else 0
    signal = alert.get('signal_strength', 0) if isinstance(alert.get('signal_strength'), int) else 0
    
    summaries = {
        'low battery': f"Battery critically low ({battery}%). Immediate device charging required.",
        'weak signal': f"Signal strength degraded ({signal}%). Check device location and connectivity.",
        'offline': "Device is offline. Verify power supply and network connection.",
        'high temperature': "Temperature reading abnormal. Check device sensors and patient status.",
        'communication error': "Unable to communicate with device. Restart device or contact support.",
    }
    
    for key, summary in summaries.items():
        if key in alert_type:
            return summary
    
    # Default fallback
    return f"{severity.capitalize()} severity alert: {alert.get('message', 'Device requires attention')}"


def generate_batch_summary(alerts: list) -> dict:
    """Generate a summary for multiple alerts"""
    
    if not alerts:
        return {"total": 0, "critical": 0, "high": 0, "summary": "No active alerts."}
    
    critical_count = len([a for a in alerts if a.get('severity') == 'Critical'])
    high_count = len([a for a in alerts if a.get('severity') == 'High'])
    
    alert_types = {}
    for alert in alerts:
        alert_type = alert.get('alert_type', 'Unknown')
        alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
    
    summary_text = f"Total: {len(alerts)} alerts | Critical: {critical_count} | High: {high_count} | "
    summary_text += " | ".join([f"{k}: {v}" for k, v in list(alert_types.items())[:3]])
    
    return {
        "total": len(alerts),
        "critical": critical_count,
        "high": high_count,
        "by_type": alert_types,
        "summary": summary_text
    }
