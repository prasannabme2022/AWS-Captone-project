# Debugging Missing Appointments

I have added a special debug tool to your application to solve the "No appointments for today" issue.

## 1. Restart Server
You MUST restart the server for the new debug tool to work.
```bash
# In your terminal
# Press Ctrl+C to stop
python aws_setup.py
```

## 2. Open Debug Page
Open this URL in your browser:
[http://127.0.0.1:5000/debug_data](http://127.0.0.1:5000/debug_data)

## 3. What to Look For
You will see a JSON response. Look for the `visibility_analysis` section.

### Scenario A: `all_appointments` is empty `[]`
- **Cause:** Since you don't have AWS credentials connected, the app uses **in-memory storage**.
- **Problem:** Every time you restart the server, **ALL DATA IS WIPED**.
- **Solution:** You must Book the Appointment **AFTER** the final server restart. 
   1. Restart Server.
   2. Log in as Patient -> Book Appointment.
   3. Log in as Doctor -> Check Dashboard.

### Scenario B: Appointments exist but `visible_on_dashboard` is `false`
- **Cause:** Date mismatch.
- **Check:** Look at `server_today_ist` vs `date_stored`.
- **Example:** Server thinks today is `2026-02-06` but appointment is `2026-02-07`.

## 4. How to Fix (If Data Wiping is the Issue)
Since you are testing locally without a persistent database:
1. **Restart Server** (Clean slate)
2. **Log in as Doctor first** (Create session)
3. **Log in as Patient** (Incognito or different browser) -> **Book Appointment**
4. **Refresh Doctor Dashboard**
5. You should see the appointment.

**Do NOT restart the server between booking and checking.**
