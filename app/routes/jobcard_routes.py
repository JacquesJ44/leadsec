from flask import request, jsonify, send_file
from datetime import datetime
from app.routes import api_bp
from app.models import db, JobCard, InvoiceImage
from app.utils.email_service import send_jobcard_confirmation
from app.utils.pdf_service import generate_jobcard_pdf
import os
import tempfile
import base64
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

@api_bp.route('/jobcards', methods=['POST'])
@login_required
def create_jobcard():
    """Create a new jobcard"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_title', 'client_name', 'client_email', 'service_location', 'technician_name', 'service_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create jobcard
        jobcard = JobCard(
            job_title=data['job_title'],
            job_description=data.get('job_description'),
            client_name=data['client_name'],
            client_email=data['client_email'],
            client_phone=data.get('client_phone'),
            service_location=data['service_location'],
            technician_name=data['technician_name'],
            service_date=datetime.fromisoformat(data['service_date']).date(),
            labor_hours=data.get('labor_hours'),
            materials_used=data.get('materials_used'),
            cost_estimate=data.get('cost_estimate'),
            notes=data.get('notes'),
            client_signature=data.get('client_signature'),
            signature_timestamp=datetime.utcnow() if data.get('client_signature') else None,
            created_by=(current_user.username if getattr(current_user, 'is_authenticated', False) else data.get('created_by', 'unknown'))
        )
        
        db.session.add(jobcard)
        db.session.commit()
        
        # Generate PDF
        temp_pdf_path = None
        try:
            temp_dir = tempfile.gettempdir()
            temp_pdf_path = os.path.join(temp_dir, f'jobcard_{jobcard.id}.pdf')
            generate_jobcard_pdf(jobcard, temp_pdf_path)
            
            # Send confirmation email
            send_jobcard_confirmation(jobcard, temp_pdf_path)
        except Exception as e:
            print(f"Error generating PDF or sending email: {str(e)}")
        finally:
            # Clean up temp file
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    os.remove(temp_pdf_path)
                except:
                    pass
        
        return jsonify({
            'message': 'Jobcard created successfully',
            'jobcard': jobcard.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>', methods=['GET'])
@login_required
def get_jobcard(jobcard_id):
    """Retrieve a specific jobcard"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        return jsonify(jobcard.to_dict(include_images=True)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards', methods=['GET'])
@login_required
def get_jobcards():
    """Retrieve all jobcards with optional filtering"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = JobCard.query
        
        if status:
            query = query.filter_by(status=status)
        
        # Pagination
        paginated = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'jobcards': [jc.to_dict() for jc in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>', methods=['PUT'])
@login_required
def update_jobcard(jobcard_id):
    """Update a jobcard"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['job_title', 'job_description', 'status', 'notes', 'labor_hours', 'cost_estimate']
        for field in allowed_fields:
            if field in data:
                setattr(jobcard, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Jobcard updated successfully',
            'jobcard': jobcard.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>/pdf', methods=['GET'])
@login_required
def download_jobcard_pdf(jobcard_id):
    """Download jobcard as PDF"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        # Generate PDF in memory
        pdf_buffer = generate_jobcard_pdf(jobcard)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'jobcard_{jobcard_id}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>/images', methods=['POST'])
@login_required
def upload_invoice_images(jobcard_id):
    """Upload invoice images for a jobcard"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        # Check if files were provided
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_images = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Validate file is an image
            if not file.content_type.startswith('image/'):
                return jsonify({'error': f'File {file.filename} is not an image'}), 400
            
            # Read and encode image as base64
            file.seek(0)
            image_data = base64.b64encode(file.read()).decode('utf-8')
            
            # Create invoice image record
            invoice_image = InvoiceImage(
                jobcard_id=jobcard_id,
                image_data=image_data,
                filename=secure_filename(file.filename),
                send_to_client=False
            )
            
            db.session.add(invoice_image)
            uploaded_images.append(invoice_image)
        
        db.session.commit()
        
        return jsonify({
            'message': f'{len(uploaded_images)} image(s) uploaded successfully',
            'images': [img.to_dict() for img in uploaded_images]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>/images', methods=['GET'])
@login_required
def get_jobcard_images(jobcard_id):
    """Get all images for a jobcard"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        images = InvoiceImage.query.filter_by(jobcard_id=jobcard_id).all()
        
        return jsonify({
            'images': [img.to_dict() for img in images]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/images/<int:image_id>', methods=['PUT'])
@login_required
def update_image_send_to_client(image_id):
    """Update whether an image should be sent to client"""
    try:
        image = InvoiceImage.query.get(image_id)
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        data = request.get_json()
        
        if 'send_to_client' in data:
            image.send_to_client = data['send_to_client']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Image updated successfully',
            'image': image.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    """Delete an invoice image"""
    try:
        image = InvoiceImage.query.get(image_id)
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({
            'message': 'Image deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/jobcards/<int:jobcard_id>/send-to-client', methods=['POST'])
@login_required
def send_jobcard_to_client(jobcard_id):
    """Send jobcard confirmation email with selected images to client"""
    try:
        jobcard = JobCard.query.get(jobcard_id)
        if not jobcard:
            return jsonify({'error': 'Jobcard not found'}), 404
        
        if not jobcard.client_email:
            return jsonify({'error': 'Client email address not found'}), 400
        
        # Generate PDF temporarily
        temp_pdf_path = None
        try:
            temp_dir = tempfile.gettempdir()
            temp_pdf_path = os.path.join(temp_dir, f'jobcard_{jobcard.id}.pdf')
            generate_jobcard_pdf(jobcard, temp_pdf_path)
            
            # Send confirmation email
            send_jobcard_confirmation(jobcard, temp_pdf_path)
            
            return jsonify({
                'message': f'Jobcard sent to {jobcard.client_email} successfully'
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to send email: {str(e)}'}), 500
        finally:
            # Clean up temp file
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    os.remove(temp_pdf_path)
                except:
                    pass
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200
