# 🚀 Quick Start Guide - Leadsec JobCard System

Follow these steps to get the system up and running.

## Phase 1: Prerequisites (One-time Setup)

### Install System Requirements
- ✅ **Python 3.8+** - Download from python.org
- ✅ **Node.js 16+** - Download from nodejs.org  
- ✅ **PostgreSQL 12+** - Download from postgresql.org or use `brew install postgresql` on Mac

### Verify Installations
```bash
python3 --version
node --version
npm --version
psql --version
```

---

## Phase 2: Backend Setup

### 1. Navigate to Backend Directory
```bash
cd /Users/jacquesdutoit/Developer/leadsec
```

### 2. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your:
# - PostgreSQL credentials
# - Email (Gmail SMTP)
# - Frontend URL
```

### 5. Create Database
```bash
python create_db.py
```

### 6. Create Admin User
```bash
python create_admin.py
```

Follow the prompts to create your first admin user account. You'll need to enter:
- Username (must be unique)
- Email address
- Password

### 7. Start Backend Server
```bash
python run.py
```

✅ Backend running on `http://localhost:5000`

---

## Phase 3: Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd /Users/jacquesdutoit/Developer/leadsec/leadsec-fe-vite
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Create Environment File
```bash
echo "VITE_API_URL=http://localhost:5000/api" > .env
```

### 4. Start Development Server
```bash
npm run dev
```

✅ Frontend running on `http://localhost:5173`

---

## Phase 4: Test the System

### 1. Open Frontend
Visit: `http://localhost:5173`

### 2. Login
- Login page will appear
- Enter the username and password you created in Phase 2, Step 6
- Click **Sign in**

### 3. Fill Out JobCard Form
- Enter job details
- Add client information
- Upload invoice images (optional)
- Sign the form with your mouse/touch
- Submit

### 4. Verify Results
- ✅ Form submits successfully
- ✅ PDF generated and downloaded
- ✅ Email sent to client (check spam folder)
- ✅ Data stored in database

---

## 📋 Configuration Checklist

### PostgreSQL Setup
- [ ] PostgreSQL server running
- [ ] Database 'leadsec' created (or `python create_db.py` run)
- [ ] PostgreSQL user accessible (default: postgres with password 'password')

### Email Configuration (for sending copies to clients)
- [ ] Gmail account with 2FA enabled
- [ ] [App Password](https://myaccount.google.com/apppasswords) generated
- [ ] MAIL_USERNAME set in .env
- [ ] MAIL_PASSWORD set in .env

### Environment Variables
```bash
# Backend .env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/leadsec
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:5173

# Frontend .env
VITE_API_URL=http://localhost:5000/api
```

---

## 🧪 Testing API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Create JobCard
```bash
curl -X POST http://localhost:5000/api/jobcards \
  -H "Content-Type: application/json" \
  -d @sample_jobcard.json
```

### Get JobCard
```bash
curl http://localhost:5000/api/jobcards/1
```

### Download PDF
```bash
curl http://localhost:5000/api/jobcards/1/pdf --output jobcard_1.pdf
```

---

## 🐛 Troubleshooting

### Backend Issues
| Problem | Solution |
|---------|----------|
| Port 5000 in use | Kill process: `lsof -ti:5000 \| xargs kill -9` |
| PostgreSQL connection error | Verify credentials in .env, ensure PostgreSQL running |
| No module named 'flask' | Activate venv: `source venv/bin/activate` |
| Email not sending | Check MAIL_* settings, verify Gmail App Password |

### Frontend Issues
| Problem | Solution |
|---------|----------|
| Port 5173 in use | Kill process: `lsof -ti:5173 \| xargs kill -9` |
| Cannot connect to API | Verify backend running, check VITE_API_URL |
| Signature not working | Check browser console for errors |

---

## 📁 Project Structure

```
/Users/jacquesdutoit/Developer/leadsec/
├── leadsec-fe-vite/          ← Frontend (React + Vite)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── app/                       ← Backend (Flask)
│   ├── models/
│   ├── routes/
│   └── utils/
├── config.py
├── requirements.txt
├── create_db.py
├── run.py
├── .env.example
└── README.md
```

---

## 🎯 Next Steps

1. **Development**: Customize form fields as needed
2. **Testing**: Test with real client data
3. **Email**: Configure email sending
4. **Deployment**: Deploy to production when ready
5. **Database**: Regular backups of jobcard data

---

## 📚 Additional Resources

- **Backend Docs**: See `README.md` in `/leadsec`
- **Frontend Docs**: See `README.md` in `/leadsec/leadsec-fe-vite`
- **Full Guide**: See `PROJECT_GUIDE.md`

---

## 💡 Tips

- **Offline Draft**: The form data is auto-saved to browser local storage
- **Mobile Testing**: Use Chrome DevTools device emulation for tablet/mobile testing
- **PDF Storage**: PDFs are generated server-side and can be stored/archived
- **Database Backup**: Regular SQL backups recommended

---

**Status**: ✅ Ready for development and testing!
