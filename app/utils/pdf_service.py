from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import base64
import os
from io import BytesIO

def generate_jobcard_pdf(job_card, output_path=None):
    """
    Generate a PDF of the jobcard with signature
    
    Args:
        job_card: JobCard model instance
        output_path: Path to save the PDF. If None, returns BytesIO object
    
    Returns:
        str or BytesIO: Path to saved file or BytesIO object
    """
    
    # Create PDF
    if output_path:
        doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    else:
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2e5090'),
        spaceAfter=12,
        spaceBefore=12,
        borderPadding=5
    )
    
    # Title
    story.append(Paragraph("JOB CARD", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Job Information Table
    story.append(Paragraph("Job Information", heading_style))
    
    job_data = [
        ['Field', 'Details'],
        ['Job Title', job_card.job_title],
        ['Description', job_card.job_description or 'N/A'],
        ['Service Date', str(job_card.service_date)],
        ['Service Location', job_card.service_location],
    ]
    
    job_table = Table(job_data, colWidths=[1.5*inch, 4.5*inch])
    job_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(job_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Client Information
    story.append(Paragraph("Client Information", heading_style))
    
    client_data = [
        ['Field', 'Details'],
        ['Client Name', job_card.client_name],
        ['Email', job_card.client_email],
        ['Phone', job_card.client_phone or 'N/A'],
    ]
    
    client_table = Table(client_data, colWidths=[1.5*inch, 4.5*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(client_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Service Details
    story.append(Paragraph("Service Details", heading_style))
    
    details_data = [
        ['Field', 'Details'],
        ['Technician', job_card.technician_name],
        ['Labor Hours', str(job_card.labor_hours) if job_card.labor_hours else 'N/A'],
        ['Materials Used', job_card.materials_used or 'N/A'],
        ['Cost Estimate', f"${job_card.cost_estimate}" if job_card.cost_estimate else 'N/A'],
    ]
    
    details_table = Table(details_data, colWidths=[1.5*inch, 4.5*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Notes
    if job_card.notes:
        story.append(Paragraph("Notes", heading_style))
        story.append(Paragraph(job_card.notes, styles['BodyText']))
        story.append(Spacer(1, 0.3*inch))
    
    # Invoice Images Section - only those marked for client
    relevant_images = [img for img in job_card.images if img.send_to_client]
    if relevant_images:
        story.append(Paragraph("Invoice & Reference Images", heading_style))
        
        # Add images in a 2-column layout
        for i, image_record in enumerate(relevant_images):
            if i > 0 and i % 2 == 0:
                story.append(PageBreak())
            
            try:
                # Decode base64 image
                image_data = base64.b64decode(image_record.image_data)
                img = Image(BytesIO(image_data), width=3.5*inch, height=3.5*inch)
                story.append(img)
                story.append(Paragraph(f"<b>{image_record.filename}</b>", styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
            except Exception as e:
                story.append(Paragraph(f"Image unavailable: {image_record.filename}", styles['BodyText']))
                story.append(Spacer(1, 0.2*inch))
        
        story.append(Spacer(1, 0.3*inch))
    
    # Signature Section
    story.append(Paragraph("Client Signature", heading_style))
    
    if job_card.client_signature:
        try:
            # Decode base64 signature and add to PDF
            signature_data = base64.b64decode(job_card.client_signature.split(',')[1])
            signature_img = Image(BytesIO(signature_data), width=2*inch, height=1*inch)
            story.append(signature_img)
        except Exception as e:
            story.append(Paragraph("Signature image unavailable", styles['BodyText']))
    else:
        story.append(Paragraph("No signature on file", styles['BodyText']))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Signed: {job_card.signature_timestamp.strftime('%Y-%m-%d %H:%M:%S') if job_card.signature_timestamp else 'N/A'}", styles['BodyText']))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer = Paragraph(f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Job Card ID: {job_card.id}</i>", styles['Normal'])
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    
    if output_path:
        return output_path
    else:
        pdf_buffer.seek(0)
        return pdf_buffer
