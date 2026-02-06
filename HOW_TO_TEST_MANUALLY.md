# How to Test Appointment Request Acceptance

## ⚠️ Important Note
You are currently viewing the **Doctor Dashboard**. The "Accept Request" feature is for **Patients**.

To see the feature, you must log in as a **Patient**.

## Step-by-Step Testing Guide

### 1. Log Out of Doctor Account
- Click the **Logout** button in the sidebar.

### 2. Log In as a Patient
- **Email:** `prasanna.sittampalam@gmail.com` (or any registered patient email)
- **Password:** `password` (or your set password)

### 3. Check the Dashboard
- Once logged in, look at the top of the dashboard.
- If a doctor has sent you a request, you will see a **yellow banner** titled "Pending Doctor Requests".
- Since this is a new feature, the list might be empty initially.

### 4. Create a Test Request (Since you are testing)
Since you cannot send a request from the UI yet (that's the next feature to build for doctors), you can use this curl command to simulate a doctor sending a request:

```bash
curl -X POST http://127.0.0.1:5000/api/appointment_request/send \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_DOCTOR_SESSION_COOKIE" \
  -d '{
    "patient_email": "prasanna.sittampalam@gmail.com",
    "proposed_date": "2026-02-15 10:00:00",
    "reason": "Routine Checkup"
  }'
```

*Note: The command above requires a valid doctor session cookie. The easiest way is to implement the "Send Request" button in the Doctor Dashboard next.*

## ✅ Code Verification Status
I have run a code verification script (`verify_acceptance.py`) which confirmed:
- **Backend APIs:** Active and working
- **Database Table:** Configured
- **Patient Dashboard UI:** Code is deployed and ready

The feature is active, but you won't see it until there is actual data (a pending request) to display.
