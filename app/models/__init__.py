from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text
from datetime import datetime

db = SQLAlchemy()

class JobCard(db.Model):
    """JobCard model for storing submitted job information"""
    __tablename__ = 'jobcards'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text)
    client_name = db.Column(db.String(255), nullable=False)
    client_email = db.Column(db.String(255), nullable=False)
    client_phone = db.Column(db.String(20))
    service_location = db.Column(db.Text, nullable=False)
    
    # Worker/Technician info
    technician_name = db.Column(db.String(255), nullable=False)
    
    # Job details
    service_date = db.Column(db.Date, nullable=False)
    labor_hours = db.Column(db.Float)
    materials_used = db.Column(db.Text)
    cost_estimate = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)
    
    # Signature - stored as base64
    client_signature = db.Column(db.Text)
    signature_timestamp = db.Column(db.DateTime)
    
    # Metadata
    status = db.Column(db.String(50), default='pending')  # pending, approved, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(255))  # User who created the jobcard
    
    # Relationship to images
    images = db.relationship('InvoiceImage', backref='jobcard', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_images=False):
        """Convert model to dictionary"""
        data = {
            'id': self.id,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'client_phone': self.client_phone,
            'service_location': self.service_location,
            'technician_name': self.technician_name,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'labor_hours': float(self.labor_hours) if self.labor_hours else None,
            'materials_used': self.materials_used,
            'cost_estimate': float(self.cost_estimate) if self.cost_estimate else None,
            'notes': self.notes,
            'has_signature': bool(self.client_signature),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        
        if include_images:
            data['images'] = [img.to_dict() for img in self.images]
        
        return data


class InvoiceImage(db.Model):
    """InvoiceImage model for storing supplier invoice photos"""
    __tablename__ = 'invoice_images'
    
    id = db.Column(db.Integer, primary_key=True)
    jobcard_id = db.Column(db.Integer, db.ForeignKey('jobcards.id'), nullable=False)
    
    # Image data stored as base64
    image_data = db.Column(Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    
    # Flag to indicate if this image should be sent to client
    send_to_client = db.Column(db.Boolean, default=False)
    
    # Metadata
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'jobcard_id': self.jobcard_id,
            'filename': self.filename,
            'image_data': self.image_data,
            'send_to_client': self.send_to_client,
            'upload_timestamp': self.upload_timestamp.isoformat(),
        }


# Simple User model for authentication
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
