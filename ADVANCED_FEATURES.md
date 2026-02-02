# 🚀 MedTrack: Advanced Level Requirements
## (Constrained to EC2, DynamoDB, & SNS)

Since this project is strictly limited to **Amazon EC2, Amazon DynamoDB, and Amazon SNS**, "Advanced" text implies high-complexity software engineering patterns implemented within the application logic rather than using managed services like Lambda or SageMaker.

Below are the detailed technical requirements for implementing these advanced features.

---

## 1. 🛡️ HIPAA-Grade Audit & Security Logging
**Goal:** strict compliance and security monitoring without external tools.

### Functional Requirements:
- **Immutable Log:** Every write operation (Create/Update/Delete) must generate a parallel log entry.
- **Traceability:** Logs must record *Who* (User email), *When* (Timestamp), *What* (Action), and *Where* (IP Address).
- **Read-Only Access:** Regular users cannot see these logs; only Super Admins can.

### Technical Requirements:
- **Database Schema:** New DynamoDB Table `medtrack_audit_logs`.
  - `PK`: `log_id` (UUID)
  - `Attributes`: `user`, `action`, `resource_id`, `timestamp`, `ip_hash`.
- **Backend Logic:** Implement a Python **Flask Decorator** (`@audit_log`) that wraps sensitive routes.
- **Security:** Logs must never optionally capture password text or sensitive health data fields (PII masking).

---

## 2. ⚡ Optimistic Concurrency Control
**Goal:** Prevent data corruption when two doctors edit the same patient file simultaneously.

### Functional Requirements:
- **Conflict Detection:** If User A views a record, and User B updates it before User A saves, User A's save must fail with a helpful message.
- **Data Integrity:** No "last write wins" - prevents accidental overwriting of new diagnosis notes.

### Technical Requirements:
- **Database Schema:** Add `version` (Number) attribute to `medtrack_patients` and `medtrack_appointments`.
- **Backend Logic:**
  - On **Read**: Fetch the current `version`.
  - On **Write**: Use DynamoDB `ConditionExpression` -> `attribute_exists(id) AND version = :read_version`.
  - On **Success**: Increment `version` by 1.
  - On **Failure**: Catch `ConditionalCheckFailedException` and return 409 Conflict.

---

## 3. 📉 Custom Analytics Engine
**Goal:** Real-time business intelligence without using QuickSight or external analytics tools.

### Functional Requirements:
- **Admin Dashboard:** Visual summary of:
  - Appointments per Day (Last 7 days).
  - Disease/Symptom Trends (e.g., "High fever cases increasing").
  - Blood Bank Critical Stock alerts.
- **Performance:** Dashboards must load in <2 seconds.

### Technical Requirements:
- **Database:** Use **Global Secondary Indexes (GSI)** on DynamoDB.
  - Index: `status-date-index` (PK: `status`, SK: `date`) to quickly query "completed" appointments.
- **Compute:** Implement Python Pandas/NumPy logic on the EC2 instance to aggregate raw data into summary stats (Count, GroupBy) before sending to frontend.

---

## 4. ⏰ Application-Layer Scheduler
**Goal:** Automated reminders without using AWS Lambda or EventBridge.

### Functional Requirements:
- **Appointment Reminders:** Send an SNS SMS/Email 24 hours before an appointment.
- **Cleanup:** Automatically archive or flag "Pending" appointments that passed their date as "Missed".

### Technical Requirements:
- **Compute:** Run a background process (using `APScheduler` or Python `threading`) inside the Flask application on EC2.
- **Logic:**
  - Run job every hour.
  - Query DynamoDB for `appointment_date == tomorrow`.
  - Trigger `sns_client.publish` for each match.
- **Resilience:** Ensure the thread restarts if the application crashes (via Gunicorn/Systemd config).

---

## 5. 🏥 Advanced Search & Filtering
**Goal:** Efficient patient lookup in large datasets.

### Functional Requirements:
- **Multi-parameter Search:** Find patients by Name, Phone, OR Blood Group.
- **Pagination:** Don't load all 10,000 records; load 20 at a time.

### Technical Requirements:
- **Database:** Efficient DynamoDB `Query` operations (not `Scan`).
- **Indexing:** Inverted Index table or multiple GSIs to support different access patterns.

---

## Summary of Architecture
- **EC2:** Handles Web Serving + Business Logic + Scheduler + Analytics Processing.
- **DynamoDB:** Handles Data Storage + Concurrency State + Audit Logs.
- **SNS:** Handles Outbound Communication (Reminders, Alerts).

This architecture proves **Advanced Python/Cloud proficiency** by building robust system features manually where managed services are restricted.
