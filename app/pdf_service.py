from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from datetime import datetime
import io


def generate_device_report_pdf(devices: list, report_title: str = "Device Health Report") -> bytes:
    """Generate a PDF report of device health data"""
    
    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey
    )
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Prepare table data
    table_data = [['Device ID', 'Patient ID', 'Type', 'Status', 'Battery', 'Signal', 'Last Sync']]
    
    for device in devices:
        table_data.append([
            device.get('device_id', ''),
            device.get('patient_id', ''),
            device.get('device_type', ''),
            device.get('status', ''),
            f"{device.get('battery_level', 0)}%",
            f"{device.get('signal_strength', 0)}%",
            device.get('last_sync', '')
        ])
    
    # Create table
    table = Table(table_data, colWidths=[1*inch, 1*inch, 1.2*inch, 0.9*inch, 0.8*inch, 0.8*inch, 1.2*inch])
    
    # Style table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    
    # Get PDF bytes
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


def generate_alert_summary_pdf(alerts: list, report_title: str = "Alert Summary Report") -> bytes:
    """Generate a PDF report of alerts"""
    
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#d32f2f'),
        spaceAfter=30,
        alignment=1
    )
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary stats
    critical_count = len([a for a in alerts if a.get('severity') == 'Critical'])
    high_count = len([a for a in alerts if a.get('severity') == 'High'])
    
    stats_text = f"<b>Total Alerts:</b> {len(alerts)} | <b>Critical:</b> {critical_count} | <b>High:</b> {high_count}"
    story.append(Paragraph(stats_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Alerts table
    table_data = [['Device ID', 'Alert Type', 'Severity', 'Message', 'Created']]
    
    for alert in alerts:
        table_data.append([
            alert.get('device_id', ''),
            alert.get('alert_type', ''),
            alert.get('severity', ''),
            alert.get('message', ''),
            alert.get('created_at', '')
        ])
    
    table = Table(table_data, colWidths=[1*inch, 1.2*inch, 1*inch, 2.5*inch, 1.3*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(table)
    doc.build(story)
    
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
