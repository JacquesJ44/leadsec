# JobCard Form System - Complete Setup Guide

A full-stack application for creating, signing, and managing job cards on-site.

## 🏗️ Architecture

### Backend (Flask)
- RESTful API for jobcard management
- MySQL database for data persistence
- PDF generation and email delivery
- Digital signature support

### Frontend (React + Vite)
- Responsive form for data entry
- Digital signature capture
- Real-time validation
- Automatic client email with PDF

### Database (MySQL)
- Structured jobcard storage
- Client information tracking
- Signature and metadata storage

## 📁 Project Structure

```
leadsec/
├── leadsec-fe-vite/          # React + Vite frontend
│   ├── src/
│   │   ├── components/        # Form and signature components
│   │   ├── utils/             # API client utilities
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── app/                       # Flask backend
│   ├── models/                # Database models
│   ├── routes/                # API endpoints
│   ├── utils/                 # Email and PDF services
│   └── __init__.py
│
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── create_db.py              # Database initialization
├── run.py                    # Backend entry point
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### Backend Setup

```bash
cd /Users/jacquesdutoit/Developer/leadsec

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Create database
python create_db.py

# Start API
python run.py
```

The API will run on `http://localhost:5000`

### Frontend Setup

```bash
cd leadsec-fe-vite

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## 📝 Features

### Authentication
- ✅ User login system with session management
- ✅ Protected routes requiring authentication
- ✅ Session persistence across browser sessions
- ✅ Logout functionality
- ✅ User context in component hierarchy

### JobCard Form
- ✅ Job title and description
- ✅ Client information (name, email, phone)
- ✅ Service location and date
- ✅ Technician assignment
- ✅ Labor hours tracking
- ✅ Materials listing
- ✅ Cost estimation
- ✅ Additional notes

### Digital Signature
- ✅ On-site signature capture
- ✅ Base64 encoding for database storage
- ✅ PDF inclusion with signature

### Image Management
- ✅ Multiple invoice/reference photo upload
- ✅ Image preview and selection
- ✅ Mark images to send to client
- ✅ Images embedded in PDF with client email
- ✅ Delete/manage images after upload

### Processing & Communication
- ✅ Form validation
- ✅ PDF generation with ReportLab
- ✅ Automatic email to client on jobcard creation
- ✅ Manual "Send to Client" button for re-sending
- ✅ Selective image inclusion in emails
- ✅ Data storage in MySQL
- ✅ Status tracking (pending/approved/completed)

## 🔌 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/register` | Register new user |
| GET | `/api/auth/me` | Get current user |

### JobCard Endpoints (all require authentication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jobcards` | Create new jobcard |
| GET | `/api/jobcards` | List all jobcards |
| GET | `/api/jobcards/<id>` | Get specific jobcard |
| PUT | `/api/jobcards/<id>` | Update jobcard |
| GET | `/api/jobcards/<id>/pdf` | Download PDF |
| POST | `/api/jobcards/<id>/send-to-client` | Send to client (resend) |

### Image Management Endpoints (all require authentication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jobcards/<id>/images` | Upload images |
| GET | `/api/jobcards/<id>/images` | Get all images |
| PUT | `/api/images/<id>` | Update image (send_to_client flag) |
| DELETE | `/api/images/<id>` | Delete image |

## 📧 Email Configuration

### Using Gmail
1. Enable 2-factor authentication on Gmail account
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Add to `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@leadsec.com
```

### Using Other SMTP Services
Update the `MAIL_SERVER`, `MAIL_PORT`, and authentication credentials in `.env`

## 🗄️ Database Schema

### users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### jobcards Table
```sql
CREATE TABLE jobcards (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_title VARCHAR(255) NOT NULL,
  job_description LONGTEXT,
  client_name VARCHAR(255) NOT NULL,
  client_email VARCHAR(255) NOT NULL,
  client_phone VARCHAR(20),
  service_location LONGTEXT NOT NULL,
  technician_name VARCHAR(255) NOT NULL,
  service_date DATE NOT NULL,
  labor_hours FLOAT,
  materials_used LONGTEXT,
  cost_estimate DECIMAL(10, 2),
  notes LONGTEXT,
  client_signature LONGTEXT,
  signature_timestamp DATETIME,
  status VARCHAR(50) DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by VARCHAR(255)
);
```

### invoice_images Table
```sql
CREATE TABLE invoice_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  jobcard_id INT NOT NULL,
  image_data LONGTEXT NOT NULL,
  filename VARCHAR(255) NOT NULL,
  send_to_client BOOLEAN DEFAULT FALSE,
  upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (jobcard_id) REFERENCES jobcards(id) ON DELETE CASCADE,
  INDEX idx_jobcard_id (jobcard_id)
);
```

## 🔧 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/leadsec
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=no-reply@leadsec.com
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## 📦 Dependencies

### Backend
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-CORS 4.0.0
- mysql-connector-python 8.1.0
- ReportLab 4.0.7 (PDF generation)
- python-dotenv 1.0.0

### Frontend
- React 18.2.0
- Vite 4.4.0
- Axios 1.5.0
- react-signature-canvas 1.0.6

## 🧪 Testing

### Backend Test
```bash
curl http://localhost:5000/api/health
```

### Create Test JobCard
```bash
curl -X POST http://localhost:5000/api/jobcards \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Test Job",
    "client_name": "Test Client",
    "client_email": "test@example.com",
    "service_location": "Test Location",
    "technician_name": "Test Tech",
    "service_date": "2024-02-20",
    "client_signature": "data:image/png;base64,..."
  }'
```

## 📱 Mobile Usage

The form is fully responsive and designed for on-site use:
- Works on tablets and mobile devices
- Touch-friendly signature capture
- Optimized form layout for vertical screens
- Real-time validation feedback

## 🔐 Security Considerations

- Use environment variables for sensitive data
- Enable HTTPS in production
- Validate all form inputs server-side
- Implement authentication for API endpoints
- Use secure SMTP configuration
- Sanitize user inputs to prevent XSS

## 🐛 Troubleshooting

### API Won't Start
- Check if port 5000 is available
- Verify MySQL is running
- Check .env configuration

### Frontend Won't Connect
- Verify API is running on port 5000
- Check VITE_API_URL configuration
- Ensure CORS is properly configured

### Email Not Sending
- Verify SMTP credentials
- Check Gmail App Password if using Gmail
- Review Flask error logs

### Signature Not Saving
- Check browser console for errors
- Verify base64 encoding is working
- Check database connectivity

## 🚀 Production Deployment

### Backend
1. Set `FLASK_ENV=production`
2. Use production WSGI server (Gunicorn, uWSGI)
3. Configure proper database with backups
4. Set strong `SECRET_KEY`
5. Use secure SMTP settings
6. Configure HTTPS/SSL

### Frontend
1. Run `npm run build`
2. Deploy `dist` folder to web server
3. Configure API_URL for production backend

## 📞 Support

For issues or questions, check the individual README files:
- Backend: [/leadsec/README.md](/leadsec/README.md)
- Frontend: [/leadsec/leadsec-fe-vite/README.md](/leadsec/leadsec-fe-vite/README.md)
