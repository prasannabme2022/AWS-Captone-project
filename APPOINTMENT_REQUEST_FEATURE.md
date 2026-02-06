# Doctor-to-Patient Appointment Request System

## Overview
This feature allows doctors to send appointment requests to patients, which patients can then accept or decline from their dashboard.

## Implementation Summary

### 1. Database Layer
- **New Table**: `medtrack_appointment_requests`
  - Primary Key: `request_id`
  - Fields: `doctor_email`, `patient_email`, `proposed_date`, `reason`, `status`, `created_at`, `updated_at`
  - Status values: `PENDING`, `ACCEPTED`, `DECLINED`

### 2. Backend Functions (aws_setup.py)
- `create_appointment_request()` - Doctor creates a request
- `get_appointment_request()` - Retrieve request by ID
- `get_patient_appointment_requests()` - Get all requests for a patient
- `get_doctor_appointment_requests()` - Get all requests sent by a doctor
- `accept_appointment_request()` - Patient accepts and creates appointment
- `decline_appointment_request()` - Patient declines with optional reason

### 3. API Routes
- `POST /api/appointment_request/send` - Doctor sends request
- `POST /api/appointment_request/accept/<request_id>` - Patient accepts
- `POST /api/appointment_request/decline/<request_id>` - Patient declines
- `GET /api/appointment_request/list?status=PENDING` - List requests

### 4. Frontend (Patient Dashboard)
- **Pending Requests Section**: Displays at top of dashboard when requests exist
- **Request Cards**: Show doctor name, specialization, proposed date, and reason
- **Action Buttons**: Accept (green) or Decline (red) with hover effects
- **Auto-refresh**: Reloads page after action to show updated state

### 5. SNS Notifications
- **Patient notification** when doctor sends request
- **Doctor notification** when patient accepts/declines
- Email includes all relevant details (date, reason, etc.)

## Usage Flow

### Doctor Side (To be implemented in doctor dashboard):
1. Doctor views patient list
2. Clicks "Send Appointment Request" button
3. Fills form: patient email, proposed date, reason
4. Submits request
5. Patient receives email notification

### Patient Side (Already implemented):
1. Patient logs in to dashboard
2. Sees yellow "Pending Doctor Requests" banner if requests exist
3. Reviews request details (doctor, date, reason)
4. Clicks "Accept" or "Decline"
5. If accepted: Appointment is created automatically
6. Doctor receives email notification of response

## Next Steps
To complete the feature, add to the doctor dashboard:
1. "Send Request" button in patient list or patient details view
2. Modal/form to input request details
3. View of sent requests with status tracking

## Testing
1. Create tables: Run `python3 aws_setup.py` to initialize DynamoDB tables
2. Test API: Use Postman or curl to test endpoints
3. UI Test: Log in as patient and check dashboard for requests section
