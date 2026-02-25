import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app
import os

def send_jobcard_confirmation(job_card, pdf_path=None):
    """
    Send jobcard confirmation email to client with PDF attachment
    Includes only images marked for client viewing
    
    Args:
        job_card: JobCard model instance
        pdf_path: Path to the generated PDF file
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Validate email configuration
        required_config = {
            'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
            'MAIL_PORT': current_app.config.get('MAIL_PORT'),
            'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
            'MAIL_PASSWORD': current_app.config.get('MAIL_PASSWORD'),
            'MAIL_DEFAULT_SENDER': current_app.config.get('MAIL_DEFAULT_SENDER'),
        }
        
        missing_config = [key for key, value in required_config.items() if not value]
        if missing_config:
            raise ValueError(f"Missing email configuration: {', '.join(missing_config)}. "
                           f"Please set these environment variables and restart the application.")
        
        # Validate required job card fields
        if not job_card.client_email:
            raise ValueError("Job card must have a client email address")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Job Card Confirmation - {job_card.job_title or 'N/A'}"
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = job_card.client_email
        
        # Create email body with safe field handling
        client_name = job_card.client_name or 'Valued Client'
        job_title = job_card.job_title or 'N/A'
        service_location = job_card.service_location or 'N/A'
        service_date = job_card.service_date or 'N/A'
        labor_hours = job_card.labor_hours or 'N/A'
        cost_estimate = job_card.cost_estimate or 'N/A'
        
        # Count images being sent to client
        images_included = len([img for img in job_card.images if img.send_to_client])
        images_text = f"<p><strong>Included in PDF:</strong> {images_included} reference/invoice image(s)</p>" if images_included > 0 else ""
        
        html_body = f"""
        <html>
            <body>
                <h2>Job Card Confirmation</h2>
                <p>Dear {client_name},</p>
                <p>Thank you for using our services. Here are the details of your job card:</p>
                
                <table border="1" cellpadding="10">
                    <tr><th>Field</th><th>Details</th></tr>
                    <tr><td>Job Title</td><td>{job_title}</td></tr>
                    <tr><td>Service Location</td><td>{service_location}</td></tr>
                    <tr><td>Service Date</td><td>{service_date}</td></tr>
                    <tr><td>Labor Hours</td><td>{labor_hours}</td></tr>
                    <tr><td>Cost Estimate</td><td>${cost_estimate}</td></tr>
                </table>
                
                {images_text}
                
                <p>Please find the attached PDF for your records.</p>
                <p>If you have any questions, please don't hesitate to contact us.</p>
                
                <p>Best regards,<br>Leadsec Team</p>
            </body>
        </html>
        """
        
        part = MIMEText(html_body, 'html')
        msg.attach(part)
        
        # Attach PDF if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= jobcard_{job_card.id}.pdf')
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
