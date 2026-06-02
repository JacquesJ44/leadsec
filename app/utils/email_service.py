import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate, make_msgid
from flask import current_app
import os


def _describe_mime_part(part, depth=0):
    indent = '  ' * depth
    content_type = part.get_content_type()
    disposition = part.get_content_disposition() or 'inline'
    filename = part.get_filename() or '-'
    lines = [f"{indent}- type={content_type}, disposition={disposition}, filename={filename}"]

    if part.is_multipart():
        for child in part.get_payload():
            lines.extend(_describe_mime_part(child, depth + 1))

    return lines


def _log_email_debug(message, attachment_names):
    logger = current_app.logger
    logger.info(
        "Email prepared: subject=%s from=%s to=%s message_id=%s attachments=%s",
        message.get('Subject'),
        message.get('From'),
        message.get('To'),
        message.get('Message-ID'),
        ', '.join(attachment_names) if attachment_names else 'none',
    )

    for line in _describe_mime_part(message):
        logger.info("Email MIME %s", line)

    header_snapshot = [
        f"Date: {message.get('Date')}",
        f"Message-ID: {message.get('Message-ID')}",
        f"Subject: {message.get('Subject')}",
        f"From: {message.get('From')}",
        f"To: {message.get('To')}",
        f"Content-Type: {message.get('Content-Type')}",
        f"MIME-Version: {message.get('MIME-Version')}",
    ]
    logger.info("Email headers\n%s", '\n'.join(header_snapshot))

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

        msg = MIMEMultipart('mixed')
        msg['Subject'] = f"Job Card Notification - {job_card.job_title or 'N/A'}"
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = to_address
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid(domain=current_app.config['MAIL_DEFAULT_SENDER'].split('@')[-1])

        attachment_names = []

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
        body = MIMEMultipart('alternative')
        text_body = (
            "Job Card Notification\n\n"
            f"Job Title: {job_title}\n"
            f"Service Location: {service_location}\n"
            f"Service Date: {service_date}\n"
            f"Labor Hours: {labor_hours}\n\n"
            "Please find the attached PDF for your records."
        )
        body.attach(MIMEText(text_body, 'plain'))
        body.attach(MIMEText(html_body, 'html'))
        msg.attach(body)


        # Attach PDF if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as attachment:
                pdf_filename = f'jobcard_{job_card.id}.pdf'
                part = MIMEBase('application', 'pdf')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                msg.attach(part)
                attachment_names.append(pdf_filename)

        # Attach images marked for client
        try:
            from app.models import InvoiceImage
            from base64 import b64decode
            # Query images for this jobcard with send_to_client=True
            images = InvoiceImage.query.filter_by(jobcard_id=job_card.id, send_to_client=True).all()
            for img in images:
                mime_type, _ = mimetypes.guess_type(img.filename)
                if mime_type:
                    maintype, subtype = mime_type.split('/', 1)
                else:
                    maintype, subtype = 'application', 'octet-stream'
                image_data = b64decode(img.image_data)
                image_part = MIMEBase(maintype, subtype)
                image_part.set_payload(image_data)
                encoders.encode_base64(image_part)
                image_filename = os.path.basename(img.filename)
                image_part.add_header('Content-Disposition', 'attachment', filename=image_filename)
                msg.attach(image_part)
                attachment_names.append(image_filename)
        except Exception as e:
            current_app.logger.exception("Error attaching jobcard images for email")

        if current_app.config.get('MAIL_DEBUG_LOGGING'):
            _log_email_debug(msg, attachment_names)

        # Send email
        debug_logging_enabled = current_app.config.get('MAIL_DEBUG_LOGGING')
        if debug_logging_enabled:
            current_app.logger.info(
                "Connecting to SMTP server host=%s port=%s tls=%s",
                current_app.config['MAIL_SERVER'],
                current_app.config['MAIL_PORT'],
                bool(current_app.config.get('MAIL_USE_TLS', True)),
            )

        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            if current_app.config.get('MAIL_SMTP_DEBUG'):
                server.set_debuglevel(1)

            server.ehlo()

            if current_app.config.get('MAIL_USE_TLS', True):
                if debug_logging_enabled:
                    current_app.logger.info("Starting TLS for SMTP session")
                server.starttls()
                server.ehlo()

            if current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD'):
                if debug_logging_enabled:
                    current_app.logger.info("Authenticating to SMTP server as %s", current_app.config['MAIL_USERNAME'])
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])

            refused_recipients = server.send_message(msg)
            if refused_recipients:
                current_app.logger.warning("SMTP server refused recipients: %s", refused_recipients)
            elif debug_logging_enabled:
                current_app.logger.info(
                    "SMTP server accepted message_id=%s for recipient=%s",
                    msg.get('Message-ID'),
                    to_address,
                )

        return True

    except Exception as e:
        current_app.logger.exception("Error sending jobcard confirmation email")
        return False
