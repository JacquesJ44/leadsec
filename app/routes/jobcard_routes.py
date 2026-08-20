
from flask import request, jsonify, send_file
from datetime import datetime
from app.routes import api_bp
from app.models import db, JobCard, InvoiceImage
from app.utils.pdf_service import generate_jobcard_pdf
import os
import tempfile
import base64
import threading
from io import BytesIO
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from pprint import pprint
from PIL import Image, UnidentifiedImageError


MAX_IMAGE_DIMENSION = 1600
JPEG_QUALITY = 80

def optimize_image_for_storage(file_storage):
    """Resize and recompress uploaded images to reduce DB storage footprint."""
    file_storage.seek(0)
    original_bytes = file_storage.read()
    file_storage.seek(0)

    if not original_bytes:
        return original_bytes

    try:
        with Image.open(BytesIO(original_bytes)) as img:
            source_format = (img.format or '').upper()

            if max(img.size) > MAX_IMAGE_DIMENSION:
                img.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)

            output = BytesIO()

            if source_format in {'JPEG', 'JPG'}:
                if img.mode not in {'RGB', 'L'}:
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
            elif source_format == 'PNG':
                img.save(output, format='PNG', optimize=True, compress_level=9)
            elif source_format == 'WEBP':
                img.save(output, format='WEBP', quality=JPEG_QUALITY, method=6)
            else:
                # Preserve image compatibility for uncommon formats.
                img.save(output, format=img.format or 'PNG', optimize=True)

            optimized_bytes = output.getvalue()

            # Keep the smaller version only.
            return optimized_bytes if len(optimized_bytes) < len(original_bytes) else original_bytes
    except (UnidentifiedImageError, OSError, ValueError):
        return original_bytes

@api_bp.route('/jobcards', methods=['POST'])
@login_required
def create_jobcard():
    """Create a new jobcard"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_title', 'client_name', 'service_location', 'technician_name', 'service_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create jobcard
        jobcard = JobCard(
            job_title=data['job_title'],
            job_description=data.get('job_description'),
            client_name=data['client_name'],
            service_location=data['service_location'],
            technician_name=data['technician_name'],
            service_date=datetime.fromisoformat(data['service_date']).date(),
            labor_hours=data.get('labor_hours'),
            materials_used=data.get('materials_used'),
            notes=data.get('notes'),
            created_by=(current_user.username if getattr(current_user, 'is_authenticated', False) else data.get('created_by', 'unknown'))
        )
        
        db.session.add(jobcard)
        db.session.commit()
        

        
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
        
        query = JobCard.query.order_by(JobCard.created_at.desc())
        results = query.all()
        # for jobcard in results:
        #     pprint(jobcard.to_dict())

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
        allowed_fields = ['job_title', 'job_description', 'status', 'notes', 'labor_hours', 'materials_used']
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

        # Get send_to_client flags from form (should be same length as files)
        send_to_client_flags = request.form.getlist('send_to_client_flags')
        # Convert to bool list (default to False if missing or invalid)
        send_to_client_bools = [(flag == '1' or flag == 'true' or flag == 'True') for flag in send_to_client_flags]
        # Pad/truncate to match files length
        while len(send_to_client_bools) < len(files):
            send_to_client_bools.append(False)
        if len(send_to_client_bools) > len(files):
            send_to_client_bools = send_to_client_bools[:len(files)]

        uploaded_images = []
        total_original_size = 0
        total_stored_size = 0

        for idx, file in enumerate(files):
            if file.filename == '':
                continue

            # Validate file is an image
            if not file.content_type.startswith('image/'):
                return jsonify({'error': f'File {file.filename} is not an image'}), 400

            # Re-encode image to reduce storage footprint before persisting.
            file.seek(0)
            original_bytes = file.read()
            optimized_bytes = optimize_image_for_storage(file)
            image_data = base64.b64encode(optimized_bytes).decode('utf-8')
            total_original_size += len(original_bytes)
            total_stored_size += len(optimized_bytes)

            # Set send_to_client from flags
            send_to_client = send_to_client_bools[idx] if idx < len(send_to_client_bools) else False

            # Create invoice image record
            invoice_image = InvoiceImage(
                jobcard_id=jobcard_id,
                image_data=image_data,
                filename=secure_filename(file.filename),
                send_to_client=send_to_client
            )

            db.session.add(invoice_image)
            uploaded_images.append(invoice_image)

        db.session.commit()

        reduction_percent = 0
        if total_original_size > 0:
            reduction_percent = round((1 - (total_stored_size / total_original_size)) * 100, 2)

        # Note: confirmation email is triggered explicitly via /send-to-client after
        # the frontend finishes creating the jobcard and uploading any images, so it
        # is not sent here to avoid duplicate emails.

        # Return all images for the jobcard, not just newly uploaded ones
        all_images = InvoiceImage.query.filter_by(jobcard_id=jobcard_id).all()

        return jsonify({
            'message': f'{len(uploaded_images)} image(s) uploaded successfully',
            'original_bytes': total_original_size,
            'stored_bytes': total_stored_size,
            'storage_reduction_percent': reduction_percent,
            'images': [img.to_dict() for img in all_images]
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    
    return jsonify({'status': 'ok'}), 200


@api_bp.route('/jobcards/<int:jobcard_id>/send-to-client', methods=['POST'])
@login_required
def send_jobcard_to_client(jobcard_id):
    """Manually trigger sending the jobcard email with PDF and images (async)"""
    from app.utils.email_service import send_jobcard_confirmation
    from flask import current_app

    jobcard = JobCard.query.get(jobcard_id)
    if not jobcard:
        return jsonify({'error': 'Jobcard not found'}), 404

    app = current_app._get_current_object()
    jc_id = jobcard.id

    def send_email_background(app, jc_id):
        with app.app_context():
            temp_pdf_path = None
            try:
                jc = JobCard.query.get(jc_id)
                temp_dir = tempfile.gettempdir()
                temp_pdf_path = os.path.join(temp_dir, f'jobcard_{jc.id}.pdf')
                generate_jobcard_pdf(jc, temp_pdf_path)
                send_jobcard_confirmation(jc, temp_pdf_path, force_to=os.environ.get('JOBCARD_EMAIL'))
            except Exception as e:
                print(f"Background manual email error: {str(e)}")
            finally:
                if temp_pdf_path and os.path.exists(temp_pdf_path):
                    try:
                        os.remove(temp_pdf_path)
                    except:
                        pass

    threading.Thread(target=send_email_background, args=(app, jc_id), daemon=True).start()
    return jsonify({'message': 'Email is being sent to client'}), 200
