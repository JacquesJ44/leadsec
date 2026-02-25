# Leadsec JobCard System - Backend API

Flask-based REST API for the JobCard form system with session-based authentication.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: MySQL connection string
- `MAIL_*`: Email configuration
- `FRONTEND_URL`: Frontend URL for CORS

### 3. Create Database

```bash
python create_db.py
```

Or manually create the database:

```sql
CREATE DATABASE leadsec;
```

### 4. Create an Admin User

```bash
python create_admin.py
```

Follow prompts to create your first admin user account.

### 5. Run the API

```bash
python run.py
```

The API will run on `http://localhost:5000`

## Authentication

The system uses Flask-Login for session-based authentication. Users must log in before accessing any jobcard routes.

### Login
- **POST** `/api/auth/login`
- Requires username and password
- Returns user information and sets session cookie

### Logout
- **POST** `/api/auth/logout`
- Clears session and logs user out

### Register User (if enabled)
- **POST** `/api/auth/register`
- Creates new user account

### Check Current User
- **GET** `/api/auth/me`
- Returns current authenticated user or null if not logged in

## API Endpoints

All JobCard endpoints require authentication.

### Create JobCard
- **POST** `/api/jobcards` (requires login)
- Create a new job card with signature

**Request Body:**
```json
{
  "job_title": "Plumbing Installation",
  "job_description": "Installation of new water pipes",
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "client_phone": "(555) 123-4567",
  "service_location": "123 Main St, City, State",
  "technician_name": "Jane Smith",
  "service_date": "2024-02-20",
  "labor_hours": 3.5,
  "materials_used": "PVC pipes, fittings, sealant",
  "cost_estimate": 450.00,
  "notes": "Work completed successfully",
  "client_signature": "data:image/png;base64,..."
}
```

### Get JobCard
- **GET** `/api/jobcards/<id>` (requires login)
- Retrieve a specific job card

### List JobCards
- **GET** `/api/jobcards?status=pending&page=1&per_page=10` (requires login)
- List all job cards with optional filters

### Update JobCard
- **PUT** `/api/jobcards/<id>` (requires login)
- Update job card details (status, notes, etc.)

### Download PDF
- **GET** `/api/jobcards/<id>/pdf` (requires login)
- Download job card as PDF file with selected images

### Send to Client
- **POST** `/api/jobcards/<id>/send-to-client` (requires login)
- Generates PDF and sends email to client with selected images
- Images marked with `send_to_client=true` are included

### Upload Images
- **POST** `/api/jobcards/<jobcard_id>/images` (requires login)
- Upload invoice/reference images for a jobcard

### Image Management
- **GET** `/api/jobcards/<jobcard_id>/images` - Get all images
- **PUT** `/api/images/<image_id>` - Update image preferences
- **DELETE** `/api/images/<image_id>` - Delete image

### Health Check
- **GET** `/api/health`
- Check API status (no authentication required)

## Email Configuration

To enable email notifications, configure SMTP settings:

### Gmail (Recommended for testing)
1. Enable 2-factor authentication on your Gmail account
2. Create an [App Password](https://myaccount.google.com/apppasswords)
3. In `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Database Schema

The jobcards table includes:
- Job information (title, description, location)
- Client details (name, email, phone)
- Service details (date, technician, hours, materials, cost)
- Digital signature (base64 encoded PNG)
- Status tracking (pending, approved, completed)
- Timestamps (created_at, updated_at)

## Features

- RESTful API design
- MySQL database storage
- PDF generation with ReportLab
- Email notifications with PDF attachment
- CORS enabled for frontend integration
- Comprehensive error handling
- Data validation

## Development

### Project Structure
```
leadsec/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   └── utils/               # Helper utilities (email, PDF)
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── create_db.py            # Database initialization
└── run.py                  # Entry point
```

## Testing

Test the API using curl or Postman:

```bash
# Create jobcard
curl -X POST http://localhost:5000/api/jobcards \
  -H "Content-Type: application/json" \
  -d @jobcard_data.json

# Get jobcard
curl http://localhost:5000/api/jobcards/1

# List jobcards
curl http://localhost:5000/api/jobcards

# Download PDF
curl http://localhost:5000/api/jobcards/1/pdf --output jobcard_1.pdf
```

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check DATABASE_URL in `.env`
- Verify MySQL user permissions

### Email Not Sending
- Check MAIL_* settings in `.env`
- Verify Gmail App Password if using Gmail
- Check error logs in console

### CORS Errors
- Verify FRONTEND_URL in `.env` matches your frontend URL
- Check browser console for specific error messages
