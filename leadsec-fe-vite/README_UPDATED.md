# Leadsec JobCard System - Frontend

React + Vite-based frontend for the JobCard form system with session-based authentication.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Build

```bash
npm run build
```

## Authentication

The system uses Flask-Login for session management. Users must log in before accessing any features.

### Login/Logout
- Users see a login page on first visit
- Login credentials are validated against the backend
- Session persists across page navigation
- Logout button available on all authenticated pages
- Protected routes automatically redirect to login if not authenticated

## Features

### User Experience
- Login page with credential validation
- Protected routes (automatic redirect to login if not authenticated)
- Current user display in top navigation
- Logout functionality on all pages
- Session persistence across page refreshes

### JobCard Features
- Real-time form validation
- Digital signature capture with clear/save options
- Responsive design for mobile/tablet use on-site
- Automatic email sending with PDF to client
- Invoice/reference image upload (single or multiple files)

### Image Management
- Upload multiple invoice/reference photos
- Preview uploaded images
- Mark images "Send to client" with checkbox
- Delete images before or after submission
- Selective image inclusion in client emails
- Images embedded in PDF

### Client Communication
- Automatic email on jobcard creation
- "Send to Client" button to resend anytime
- Selective image control (which images go to client)
- PDF with embedded images in email

## Project Structure

```
src/
├── App.jsx                    # Main app with routing & auth
├── contexts/
│   └── AuthContext.jsx        # Authentication context provider
├── components/
│   ├── Login.jsx              # Login page
│   ├── JobCardForm.jsx        # Form with image upload
│   ├── JobCardsList.jsx       # List of jobcards
│   ├── JobCardDetail.jsx      # Detail view with send button
│   ├── ProtectedRoute.jsx     # Route protection wrapper
│   └── SignaturePad.jsx       # Signature capture
├── hooks/
│   └── useAuth.js             # Custom auth hook
└── utils/
    └── api.js                 # API client with auth endpoints
```

## Environment Variables

Create a `.env` file with:

```
VITE_API_URL=http://localhost:5000/api
```

## API Integration

The frontend communicates with the backend API at `http://localhost:5000/api`.

### Key Endpoints Used
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user
- `POST /jobcards` - Create jobcard
- `GET /jobcards` - List jobcards
- `GET /jobcards/<id>` - Get jobcard details
- `PUT /jobcards/<id>` - Update jobcard
- `GET /jobcards/<id>/pdf` - Download PDF
- `POST /jobcards/<id>/send-to-client` - Resend to client
- `POST /jobcards/<id>/images` - Upload images
- `GET /jobcards/<id>/images` - Get images
- `PUT /images/<id>` - Update image preferences
- `DELETE /images/<id>` - Delete image

## Dependencies

- React 18.2+
- Vite 4.4+
- Axios for HTTP requests
- React Router for navigation
- React Signature Canvas for signature capture
