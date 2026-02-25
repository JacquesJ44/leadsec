# Admin & Office Staff Guide - Leadsec JobCard System

## For Management & Office Processing

This guide explains how to manage, review, and process submitted jobcards.

---

## � User Authentication & Access

### Creating Admin Users

To create the first admin user, run:
```bash
python create_admin.py
```

Follow the prompts to enter:
- Username (unique)
- Email address
- Password

### Logging In

1. Navigate to the application
2. Enter your username and password on the login page
3. Click **Sign in**
4. You now have access to all features

### Session Management

- Your session persists as you navigate the system
- Your username is displayed in the top right of each page
- To log out, click the **Sign Out** button

---

## 🖥️ Admin Dashboard Access

### Current Status
The admin dashboard is not yet built. This guide explains what's needed and how to access jobcards via the frontend.

### For Future Development
An admin dashboard will provide:
- [ ] List of all submitted jobcards
- [ ] Search and filter capabilities
- [ ] Status management (Pending → Approved → Completed)
- [ ] Client communication log
- [ ] PDF storage and retrieval
- [ ] Export reports

---

## 📊 Current Jobcard Access Methods

### Method 1: API (For Developers)

#### List All Jobcards
```bash
curl http://localhost:5000/api/jobcards
```

Response includes:
- All jobcards with pagination
- Job details and client info
- Signature status
- Current status

#### Filter by Status
```bash
curl "http://localhost:5000/api/jobcards?status=pending&page=1&per_page=10"
```

Status options:
- `pending` - New submissions
- `approved` - Ready for work/reviewed
- `completed` - Finished and closed

#### Get Specific Jobcard
```bash
curl http://localhost:5000/api/jobcards/1
```

#### Download PDF
```bash
curl http://localhost:5000/api/jobcards/1/pdf --output jobcard_1.pdf
```

### Method 2: Database Query (MySQL)

```sql
-- View all jobcards
SELECT * FROM jobcards;

-- View pending jobcards
SELECT * FROM jobcards WHERE status = 'pending' ORDER BY created_at DESC;

-- View jobcards by client
SELECT * FROM jobcards WHERE client_email = 'client@example.com';

-- View jobcards by date range
SELECT * FROM jobcards 
WHERE service_date BETWEEN '2024-01-01' AND '2024-02-29'
ORDER BY service_date DESC;

-- Get jobcard statistics
SELECT 
  COUNT(*) as total_jobcards,
  SUM(labor_hours) as total_hours,
  SUM(cost_estimate) as total_cost,
  COUNT(DISTINCT client_email) as unique_clients
FROM jobcards
WHERE service_date >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 📋 Jobcard Workflow

### Workflow States

```
┌──────────────┐
│   Submitted  │  (Technician completes and submits)
└──────┬───────┘
       ↓
┌──────────────────┐
│    Pending       │  (Admin reviews, may request changes)
└──────┬───────────┘
       ↓
┌──────────────────┐
│   Approved       │  (Verified and approved by manager)
└──────┬───────────┘
       ↓
┌──────────────────┐
│   Completed      │  (Fully processed and archived)
└──────────────────┘
```

---

## 🔄 Processing JobCards

### Step 1: Review Submission

When a new jobcard arrives:

```
Questions to Ask:
☐ Are all required fields filled?
☐ Is the signature present?
☐ Is the client information valid?
☐ Do the service details make sense?
☐ Is the cost estimate reasonable?
☐ Any follow-up needed with technician?
```

### Step 2: Update Status

Use the API to update jobcard status:

```bash
curl -X PUT http://localhost:5000/api/jobcards/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved"
  }'
```

Status values:
- `pending` - Initial state
- `approved` - Ready for next step
- `completed` - Final/archived

### Step 3: Add Notes

Add administrative notes to jobcard:

```bash
curl -X PUT http://localhost:5000/api/jobcards/1 \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Reviewed and approved. Additional note from office manager."
  }'
```

### Step 4: Archive/Complete

Once processing is done:

```bash
curl -X PUT http://localhost:5000/api/jobcards/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

---

## � Managing Client Communications

### Resending Jobcards to Clients

If you need to resend a jobcard to the client with updated images:

1. Navigate to the JobCard Detail page
2. Update which images are marked "Send to client" if needed
3. Click the **✉️ Send to Client** button
4. The email will be sent with the currently selected images

### Image Management

#### Upload Images After Creation

If images need to be added after the jobcard was created:

```bash
curl -X POST http://localhost:5000/api/jobcards/1/images \
  -F "files=@invoice1.jpg" \
  -F "files=@invoice2.png"
```

#### Mark Images for Client

To control which images are sent to the client:

```bash
curl -X PUT http://localhost:5000/api/images/5 \
  -H "Content-Type: application/json" \
  -d '{
    "send_to_client": true
  }'
```

#### Get All Images for a Jobcard

```bash
curl http://localhost:5000/api/jobcards/1/images
```

Response includes:
- Image ID
- Filename
- send_to_client status
- Upload timestamp

#### Delete an Image

```bash
curl -X DELETE http://localhost:5000/api/images/5
```

### Email Workflow

1. **Automatic Email** - When a jobcard is created, an email is automatically sent to client
2. **Manual Resend** - Click "Send to Client" button to resend anytime
3. **Image Selection** - Only images with `send_to_client=true` are included
4. **PDF Attachment** - Full jobcard PDF is attached to the email
5. **Image Embedding** - Selected images are embedded in the PDF

---

## �💼 Administrative Tasks

### Task 1: Daily Review

Every morning, check for pending jobcards:

```bash
# Get pending jobcards from last 24 hours
curl "http://localhost:5000/api/jobcards?status=pending" | grep -i created_at
```

### Task 2: Weekly Reports

#### Labor Hours Summary
```sql
SELECT 
  WEEK(service_date) as week,
  COUNT(*) as jobcards,
  SUM(labor_hours) as total_hours,
  AVG(labor_hours) as avg_hours
FROM jobcards
WHERE YEAR(service_date) = YEAR(NOW())
GROUP BY WEEK(service_date)
ORDER BY week DESC;
```

#### Revenue Summary
```sql
SELECT 
  DATE(service_date) as date,
  COUNT(*) as jobcards,
  SUM(cost_estimate) as total_cost,
  AVG(cost_estimate) as avg_cost
FROM jobcards
WHERE service_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(service_date)
ORDER BY date DESC;
```

#### Top Technicians
```sql
SELECT 
  technician_name,
  COUNT(*) as jobcards,
  SUM(labor_hours) as total_hours,
  AVG(cost_estimate) as avg_cost_per_job
FROM jobcards
WHERE service_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY technician_name
ORDER BY jobcards DESC;
```

### Task 3: Quality Assurance

Check for issues:

```sql
-- Missing required information
SELECT id, job_title, client_email, status 
FROM jobcards 
WHERE materials_used IS NULL OR cost_estimate IS NULL;

-- Unusually high labor hours
SELECT id, job_title, labor_hours, cost_estimate 
FROM jobcards 
WHERE labor_hours > 12
ORDER BY labor_hours DESC;

-- Duplicate clients same day (potential error)
SELECT client_email, service_date, COUNT(*) as count
FROM jobcards
WHERE service_date >= CURDATE()
GROUP BY client_email, service_date
HAVING count > 1;
```

### Task 4: Client Communication

#### Get client details
```sql
SELECT DISTINCT
  client_name,
  client_email,
  client_phone,
  COUNT(*) as total_jobs,
  SUM(cost_estimate) as total_cost
FROM jobcards
WHERE client_email = 'specific@client.com'
GROUP BY client_email;
```

#### Send follow-up email
Create a template for follow-up communications:

```
Subject: Follow-up on Service Provided on [DATE]

Dear [CLIENT_NAME],

We hope you are satisfied with the service provided on [DATE].

Service Details:
- Job: [JOB_TITLE]
- Location: [SERVICE_LOCATION]
- Technician: [TECHNICIAN_NAME]
- Total Cost: $[COST_ESTIMATE]

If you have any questions, please don't hesitate to contact us.

Regards,
Leadsec Team
```

---

## 🗂️ Data Management

### Backup Database

```bash
# Daily backup
mysqldump -u root -p leadsec > backup_$(date +%Y%m%d).sql

# With compression
mysqldump -u root -p leadsec | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore from Backup

```bash
mysql -u root -p leadsec < backup_20240220.sql

# From compressed backup
gunzip < backup_20240220.sql.gz | mysql -u root -p leadsec
```

### Export Reports

```bash
# Export all jobcards as CSV
mysql -u root -p leadsec -e "SELECT * FROM jobcards" > jobcards_export.csv

# Export with specific date range
mysql -u root -p leadsec -e "
SELECT * FROM jobcards 
WHERE service_date BETWEEN '2024-01-01' AND '2024-02-29'
" > jobcards_jan_feb_2024.csv
```

---

## 📧 Email Management

### Client Receipt Emails

The system automatically sends a PDF receipt to each client containing:
- Complete jobcard details
- Digital signature
- Cost estimate
- Date and technician name

### Client Email Troubleshooting

If a client didn't receive their email:

1. **Check Configuration**
   - Verify MAIL_USERNAME and MAIL_PASSWORD in backend .env
   - Test SMTP settings

2. **Resend Email**
   ```bash
   # Download and resend PDF to client
   curl http://localhost:5000/api/jobcards/1/pdf --output jobcard.pdf
   # Then manually email to client
   ```

3. **Check Gmail**
   - Verify App Password is correct (not regular password)
   - Check [Gmail activity log](https://myaccount.google.com/security-checkup)

---

## 🔒 Security & Compliance

### Data Protection
- [ ] Regular backups (daily minimum)
- [ ] Encrypted database connections
- [ ] Restricted admin access
- [ ] Audit logs for changes
- [ ] Secure password storage

### Client Privacy
- [ ] Only authorized staff access jobcards
- [ ] Don't share client emails publicly
- [ ] Secure PDF delivery (encrypted when possible)
- [ ] GDPR compliance for EU clients

### Signature Legality
- Stored digital signatures are legally binding
- Keep backups for legal reference
- Don't modify signed jobcards
- Maintain audit trail

---

## 📱 KPIs & Metrics to Track

### Performance Metrics

```sql
-- Average completion time per job
SELECT 
  ROUND(AVG(HOUR(TIME(updated_at - created_at))), 2) as avg_hours_to_complete,
  ROUND(AVG(MINUTE(TIME(updated_at - created_at))), 2) as avg_minutes
FROM jobcards 
WHERE status = 'completed'
AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Job completion rate
SELECT 
  COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
  COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
  COUNT(*) as total,
  ROUND(COUNT(CASE WHEN status = 'completed' THEN 1 END) / COUNT(*) * 100, 2) as completion_rate
FROM jobcards;

-- Revenue metrics
SELECT 
  SUM(cost_estimate) as total_revenue,
  AVG(cost_estimate) as avg_per_job,
  MIN(cost_estimate) as min_cost,
  MAX(cost_estimate) as max_cost
FROM jobcards
WHERE service_date >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 🚀 Best Practices

✅ **Do:**
- Review jobcards daily
- Keep backups updated
- Follow up on pending items quickly
- Communicate with technicians about issues
- Track metrics for improvements
- Maintain audit logs

❌ **Don't:**
- Delete jobcards without archiving
- Share client information externally
- Modify signed documents
- Ignore pending reviews
- Skip backups
- Give all staff admin access

---

## 🛠️ Future Admin Features (Roadmap)

- [ ] Web-based admin dashboard
- [ ] Real-time jobcard list
- [ ] Advanced filtering and search
- [ ] Bulk actions (update status, assign, etc.)
- [ ] Invoice generation
- [ ] Client payment tracking
- [ ] Performance analytics
- [ ] Export to accounting software
- [ ] Mobile admin app
- [ ] Automated reminders

---

## 📞 Support

### Common Issues

**Jobcard not showing in list**
- Check the status (might be filtered)
- Verify database connection
- Check date range filters

**Can't update status**
- Verify jobcard ID exists
- Check JSON format in API call
- Look for error messages

**PDF won't download**
- Ensure jobcard exists
- Check file permissions
- Try browser incognito mode

**Database issues**
- Verify MySQL is running
- Check connection credentials
- Review database logs

---

## 📚 Quick Reference Commands

```bash
# Check system health
curl http://localhost:5000/api/health

# Get all pending jobcards
curl http://localhost:5000/api/jobcards?status=pending

# Get jobcard details
curl http://localhost:5000/api/jobcards/[ID]

# Update jobcard
curl -X PUT http://localhost:5000/api/jobcards/[ID] \
  -H "Content-Type: application/json" \
  -d '{"status":"approved"}'

# Download PDF
curl http://localhost:5000/api/jobcards/[ID]/pdf --output jobcard.pdf
```

---

**Version**: 1.0
**Last Updated**: February 2024
**Status**: Ready for implementation
