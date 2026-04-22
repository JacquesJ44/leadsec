# Operational Guide - Leadsec JobCard System

## For Technicians & Site Workers

This guide explains how to use the JobCard system while on-site with clients.

---

## � User Authentication

### First Access - Login
1. Open your browser and navigate to the JobCard application
2. You will see the **Sign In** page
3. Enter your username and password
4. Click **Sign in**
5. You will be logged in for the duration of your session

### Session Persistence
- Your login session persists as you navigate between pages
- You can browse JobCards, create new ones, and manage images without logging in again
- Your username is displayed in the top right of each page

### Logout
- Click the **Sign Out** button (available on all pages) to log out
- After logging out, you must log in again to access the system

---

## 📱 Accessing the System

### On Mobile or Tablet (Recommended)
1. Open your device's web browser
2. Navigate to: `http://leadsec-app.local` or the provided URL
3. Log in with your credentials
4. The form will load and be ready to use

### On Desktop
1. Open any web browser
2. Navigate to the frontend URL
3. Log in with your credentials
4. The form is responsive and works on all screen sizes

---

## ✏️ Filling Out the JobCard Form

### 1. Job Information
| Field | Instructions |
|-------|--------------|
| **Job Title** | Enter a brief name for the job (e.g., "Plumbing Repair") |
| **Description** | Provide detailed description of work performed |
| **Service Date** | Select today's date or the date work was performed |
| **Service Location** | Enter the complete address where work was done |
| **Labor Hours** | Record total hours spent on the job |

### 2. Client Information  
| Field | Instructions |
|-------|--------------|
| **Client Name** | Full name of the person who hired you |
| **Client Email** | Email address for receipt delivery |
| **Client Phone** | Contact number (optional) |

### 3. Service Details
| Field | Instructions |
|-------|--------------|
| **Technician Name** | Your name or ID |
| **Materials Used** | List all materials/parts used (e.g., "PVC pipe, coupling, sealant") |
| **Cost Estimate** | Total cost of services and materials |
| **Additional Notes** | Any special notes about the job |

### 4. Sign Off
1. **Review Form** - Verify all information is correct
2. **Client Signature** - Have the client sign in the signature box using their finger (tablet) or mouse
3. **Signature Actions**:
   - **Clear**: Erase and re-sign if needed
   - **Save Signature**: Confirms signature is ready

### 5. Upload Invoice/Reference Images (Optional)
1. **Select Photos** - Click the file input to select one or more invoice or reference photos
2. **Image Preview** - Selected images will display as thumbnails
3. **Mark for Email Report** - Check the "Include in email report" checkbox for any images you want attached to the email
4. **Delete if Needed** - Click the delete button to remove any image before submitting
5. **Submit Jobcard** - Images will automatically upload when you submit the jobcard

### 6. Submit
- Click **Submit JobCard** button
- You will be redirected to the JobCards list on success
- A PDF and email are automatically sent in the background after image upload
- The email will include only the images you marked "Include in email report"

---

## 📧 Managing JobCards After Submission

### View JobCard Details
1. Navigate to **JobCards** list
2. Click **View** on any jobcard to see full details
3. On the detail page you can:
   - Edit job information (including Materials Used)
   - Manage images (check/uncheck "Include in email report" flag)
   - Download PDF
   - **✉️ Send Email to Client** - Click this button to send the jobcard email with currently selected images

### Send Email to Client
- After you've selected which images to include, click the **✉️ Send Email to Client** button
- The response is immediate — the email is sent in the background
- A confirmation message **"✅ Email queued — it will arrive shortly."** will appear next to the button
- This is useful if you want to resend or update which images are included

---

## ✅ Step-by-Step Workflow

```
┌─────────────────────────┐
│  Arrive at Job Site     │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Open JobCard Form       │
│ (http://localhost:5173) │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Fill in Job Details     │
│ (Description, Location) │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Enter Client Info       │
│ (Name, Email)           │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Document Service Work   │
│ (Hours, Materials, Cost)│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Upload Invoice Images   │
│ (Mark for email report) │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Review & Submit         │
└────────────┬────────────┴───┐
             ↓                 ↓
    ✅ Redirected         ⚠️ Fix Errors
    to JobCards list
             ↓
┌─────────────────────────┐
│ PDF & Email sent in     │
│ background (async)      │
└─────────────────────────┘
```

---

## 📋 Required Information Checklist

Before submitting, ensure you have:

### Job Details
- [ ] Job title/type
- [ ] Work description
- [ ] Service date
- [ ] Service location/address
- [ ] Number of hours worked

### Client Details
- [ ] Client's full name
- [ ] Client's email address

### Service Documentation
- [ ] Technician/your name
- [ ] Materials list
- [ ] Any special notes

---

## 🔧 Common Tasks

### What if I need to edit something?
1. Use the form fields to correct the information
2. The form doesn't save until you click Submit
3. Click **Clear Form** to start over completely

### What if the signature didn't capture?
1. Click the **Clear** button in the signature box
2. Have the client sign again
3. Then click **Save Signature** before submitting

### What if the internet disconnects mid-form?
1. Your form data is saved in the browser
2. When internet returns, the data will still be there
3. Complete and submit the form

### What if I submitted by mistake?
1. Contact the office
2. They can mark the jobcard as invalid or create a new one
3. Your data is still in the system for review

---

## 📄 What Happens After Submission

1. **PDF Generated** (in background after image upload)
   - Professional document created with all form data
   - Includes company logo and jobcard ID

2. **Email Sent** (in background, a few seconds after submission)
   - PDF attached as confirmation
   - Includes only images marked "Include in email report"
   - Email includes jobcard reference number

3. **Data Stored** (immediately)
   - Information saved to secure database
   - Accessible to office staff for processing
   - Can be tracked and updated

4. **Redirect to JobCards List**
   - After successful submission you are taken straight to the jobcards list
   - Open any jobcard to view, edit, manage images, or resend the email

---

## 📞 Support

### If the form won't load:
1. Check your internet connection
2. Try refreshing the page (F5 or Cmd+R)
3. Clear browser cache
4. Try a different browser

### If you can't submit:
1. Check that all required fields are filled (marked with *)
2. Verify client email is valid (user@example.com)
3. Ensure client has signed
4. Check internet connection

### If nothing works:
- Contact office immediately at [support number]
- Have ready: Your name, client name, job details
- Take a screenshot of any error messages

---

## 💡 Pro Tips

✅ **Best Practices**:
- Fill out the form immediately after completing work (while you remember details)
- Review all information before submitting
- Keep the client present while filling out form
- Use clear, legible client signatures
- Double-check client email address for typos

❌ **Common Mistakes to Avoid**:
- Don't enter wrong client email (they won't receive receipt)
- Don't fill out the form hours later (details may be forgotten)
- Don't submit without signature
- Don't forget service location details

---

## 🎯 Form Tips by Device

### Using on Tablet/iPad (Recommended)
- Portrait or landscape orientation works
- Touch-friendly signature capture
- Form fields are large and easy to tap
- Auto-zoom on text input

### Using on Mobile
- Portrait orientation is better
- Zoom in if needed for better details
- Signature works well with fingers
- Consider connecting to WiFi for faster submission

### Using on Desktop
- Form is fully usable with mouse
- Can work offline and submit when connected
- Signature requires mouse/trackpad

---

## 📊 Common Field Examples

### Job Title Examples
- "Plumbing Installation"
- "Electrical Repair"
- "HVAC Maintenance"
- "Drywall Patching"

### Service Location Example
```
123 Main Street
Apartment 4B
Springfield, IL 62701
United States
```

### Materials Used Example
```
- 25 feet of 1/2" PVC pipe
- 6 PVC elbows
- 2 couplings
- 1 can thread sealant tape
- 1 tube silicone caulk
```

### Cost Estimate Example
```
Materials: $180.00
Labor (4.5 hours @ $50/hr): $225.00
Subtotal: $405.00
Tax: $32.40
Total: $437.40
```

---

## 🔐 Data Privacy

- All jobcards are stored securely
- Client email addresses are not shared
- Only authorized staff can access jobcard data
- PDFs are encrypted before email delivery
- Signatures are legally binding

---

## ✨ Summary

The JobCard system makes it easy to:
✅ Document work on-site
✅ Get client approval instantly  
✅ Send professional receipts
✅ Track all services
✅ Maintain organized records

**Quick Reference**: Fill in → Review → Sign → Submit → Done!

---

**Last Updated**: February 2024
**Version**: 1.0
