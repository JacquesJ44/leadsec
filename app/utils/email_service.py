import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app
import os

def send_jobcard_confirmation(job_card, pdf_path=None, force_to=None):
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
        
        # Determine recipient
        to_address = force_to or current_app.config.get('JOBCARD_EMAIL')
        if not to_address:
            raise ValueError("No recipient address specified for jobcard email.")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Job Card Notification - {job_card.job_title or 'N/A'}"
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = to_address

        # Create email body
        job_title = job_card.job_title or 'N/A'
        service_location = job_card.service_location or 'N/A'
        service_date = job_card.service_date or 'N/A'
        labor_hours = job_card.labor_hours or 'N/A'

        html_body = f"""
        <html>
            <body>
                <h2>Job Card Notification</h2>
                <table border="1" cellpadding="10">
                    <tr><th>Field</th><th>Details</th></tr>
                    <tr><td>Job Title</td><td>{job_title}</td></tr>
                    <tr><td>Service Location</td><td>{service_location}</td></tr>
                    <tr><td>Service Date</td><td>{service_date}</td></tr>
                    <tr><td>Labor Hours</td><td>{labor_hours}</td></tr>
                </table>
                <p>Please find the attached PDF for your records.</p>
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
                part.add_header('Content-Disposition', f'attachment; filename=jobcard_{job_card.id}.pdf')
                msg.attach(part)

        # Attach images marked for client
        try:
            from app.models import InvoiceImage
            from base64 import b64decode
            # Query images for this jobcard with send_to_client=True
            images = InvoiceImage.query.filter_by(jobcard_id=job_card.id, send_to_client=True).all()
            for img in images:
                # Try to guess MIME type from filename
                if img.filename.lower().endswith('.jpg') or img.filename.lower().endswith('.jpeg'):
                    maintype, subtype = 'image', 'jpeg'
                elif img.filename.lower().endswith('.png'):
                    maintype, subtype = 'image', 'png'
                else:
                    maintype, subtype = 'application', 'octet-stream'
                image_data = b64decode(img.image_data)
                image_part = MIMEBase(maintype, subtype)
                image_part.set_payload(image_data)
                encoders.encode_base64(image_part)
                image_part.add_header('Content-Disposition', f'attachment; filename={img.filename}')
                msg.attach(image_part)
        except Exception as e:
            print(f"Error attaching images: {str(e)}")

        # Send email
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        if current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD'):
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
