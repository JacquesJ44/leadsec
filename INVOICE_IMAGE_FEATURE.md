# Invoice Image Upload Feature

## Overview
Added comprehensive support for uploading and managing supplier invoice photos in the jobcard system. Users can upload multiple images of invoices, and selectively choose which images to include when sending jobcard confirmations to clients.

## Features Implemented

### 1. Database Model (`app/models/__init__.py`)
- **New Table**: `invoice_images`
  - `id`: Primary key
  - `jobcard_id`: Foreign key to jobcards table
  - `image_data`: Base64-encoded image data (LongText for large images)
  - `filename`: Original filename of the uploaded image
  - `send_to_client`: Boolean flag to control which images are sent to client
  - `upload_timestamp`: When the image was uploaded

- **Updated JobCard Model**:
  - Added relationship to InvoiceImage for easy access to related images
  - Updated `to_dict()` method with optional `include_images` parameter

### 2. Backend API Routes (`app/routes/jobcard_routes.py`)

#### Image Upload
```
POST /api/jobcards/{jobcard_id}/images
- Upload multiple image files for a jobcard
- Validates that files are images
- Returns uploaded image records with IDs
```

#### Get Images
```
GET /api/jobcards/{jobcard_id}/images
- Retrieve all images associated with a jobcard
- Returns image metadata and base64 data
```

#### Update Image Preferences
```
PUT /api/images/{image_id}
- Update the `send_to_client` flag for an image
- Controls which images are included in client communications
```

#### Delete Image
```
DELETE /api/images/{image_id}
- Remove an image from the system
```

### 3. PDF Generation (`app/utils/pdf_service.py`)
- **Updated** `generate_jobcard_pdf()` to include invoice images
- Only images with `send_to_client=True` are embedded in the PDF
- Images are displayed in a section titled "Invoice & Reference Images"
- Images are formatted with proper spacing and labeled with filenames
- Multiple images are handled across multiple pages as needed

### 4. Email Service (`app/utils/email_service.py`)
- **Updated** `send_jobcard_confirmation()` to:
  - Count relevant images being sent to client
  - Display image count in confirmation email to client
  - PDF (which includes relevant images) is attached

### 5. Frontend Form (`leadsec-fe-vite/src/components/JobCardForm.jsx`)

#### New Features:
- **File Input Section**: Multi-file selector for images
- **Selected Images Preview**: Shows thumbnails of images before submitting jobcard
- **Uploaded Images Management**: After jobcard creation, displays uploaded images with:
  - Thumbnail preview
  - Filename
  - Checkbox to mark "Send to client"
  - Delete button for removal
- **Integrated Upload**: Images are automatically uploaded when jobcard is submitted
- **Error Handling**: Validates that selected files are images

#### User Workflow:
1. Fill out jobcard form as usual
2. Scroll to "Supplier Invoice & Reference Images" section
3. Click to select multiple image files
4. See preview of selected images
5. Submit jobcard (images upload automatically)
6. View uploaded images with checkboxes
7. Check boxes for images to include in client email
8. Click "Save Image Preferences" to finalize choices

### 6. Frontend Styling (`leadsec-fe-vite/src/components/JobCardForm.css`)
Added comprehensive styles for:
- File input field with dashed border
- Image grid layout (responsive, 2-4 columns)
- Image preview cards with hover effects
- Color coding: blue for selected, green for uploaded
- Checkbox styling for client selection
- Small buttons for delete actions
- Responsive design for mobile devices

### 7. API Client (`leadsec-fe-vite/src/utils/api.js`)
Added methods:
```javascript
uploadImages(jobcardId, formData)      // Upload images
getImages(jobcardId)                   // Get all images
updateImage(imageId, data)             // Update preferences
deleteImage(imageId)                   // Delete image
```

### 8. Database Migration (`migrations/versions/001_add_invoice_images_table.py`)
- Creates the `invoice_images` table
- Sets up foreign key relationship with jobcards
- Creates index on jobcard_id for query performance

## Data Flow

### Submission Process:
1. User fills jobcard form and selects images
2. Form submission creates jobcard
3. Images are uploaded to newly created jobcard
4. PDF is generated including only "send_to_client" images
5. Email is sent with PDF attachment and image count mentioned

### Image Management:
- Images are stored as base64 in database (allows easy portability)
- Each image has a flag controlling visibility to client
- Images can be deleted without affecting jobcard
- Admin can selectively include/exclude images after jobcard creation

## Benefits

1. **Flexibility**: Upload multiple photos for documentation purposes
2. **Control**: Choose which images to share with client
3. **Professional**: Invoice photos embedded directly in PDF sent to client
4. **Scalable**: Supports unlimited number of images per jobcard
5. **Non-Destructive**: Images can be managed independently from jobcard

## Future Enhancement Opportunities

1. **Image Editing**: Crop/rotate before sending
2. **Image Organization**: Tag or categorize images
3. **Batch Selection**: Select multiple images at once
4. **Image Compression**: Auto-compress before storage
5. **Admin Dashboard**: View all images across jobcards
6. **Archive System**: Keep deleted images in archive
7. **OCR**: Extract text from invoice images

## Database Migration

To apply the new table structure:

```bash
cd /Users/jacquesdutoit/Developer/leadsec
source venv/bin/activate
alembic upgrade head
```

This will create the `invoice_images` table with proper relationships.

## Send to Client Feature

### Overview
After a jobcard is created, users can manage which images are sent to clients. The "Send to Client" button allows users to resend the jobcard PDF with the currently selected images to the client's email address.

### How It Works

1. **Image Selection During Form Submission**
   - When creating a jobcard, user can mark images "Send to client"
   - Selected images are automatically emailed when jobcard is submitted
   
2. **Resending Later**
   - Users can return to the JobCard Detail page anytime
   - Check/uncheck images to control what gets sent
   - Click **✉️ Send to Client** button
   - Email is sent with updated image selection

3. **Email Contents**
   - Full jobcard details
   - PDF attachment with embedded images
   - Image count notification
   - All images marked with `send_to_client=true` included

### New API Endpoint

**POST** `/api/jobcards/<jobcard_id>/send-to-client`
- Generates PDF with selected images
- Sends email to client
- Returns confirmation message
- Requires authentication

### Frontend Implementation

**Button Location**: JobCardDetail component header
- Available after jobcard is created
- Shows **✉️ Send to Client** button
- Shows loading state during processing
- Shows success/error messages

## Testing Checklist

- [ ] Upload single image
- [ ] Upload multiple images  
- [ ] Mark image for client visibility
- [ ] Verify PDF includes marked images
- [ ] Verify email mentions image count
- [ ] Delete image from uploaded list
- [ ] Clear form resets image selection
- [ ] Images persist after jobcard creation
- [ ] Responsive layout on mobile
- [ ] Send to Client button works
- [ ] Unselected images not included in resent email
- [ ] Email sent successfully with button click
- [ ] Error handling for failed sends

## Notes

- Images are stored as base64 to avoid file system dependencies
- Max file size depends on database configuration (LongText supports large images)
- Jobcard submission does NOT require images (optional)
- Images can be managed independently of jobcard status
- Deleted images are permanently removed (no recovery)
- "Send to Client" button only available after jobcard creation
- Email is sent automatically on jobcard creation with selected images
- Users can resend anytime without recreating the jobcard
