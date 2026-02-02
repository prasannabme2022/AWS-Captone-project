
# Mock Database for Medtrack
# Using Python dictionaries for data persistence (in-memory)

# Users Data: Key = Email
users = {
    "patient@example.com": {
        "id": "p1",
        "name": "John Doe",
        "email": "patient@example.com",
        "password": "password123", # In production, hash this!
        "role": "patient"
    },
    "doctor@example.com": {
        "id": "d1",
        "name": "Dr. Smith",
        "email": "doctor@example.com",
        "password": "password123",
        "role": "doctor"
    },
    "admin@example.com": {
        "id": "a1",
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "password123",
        "role": "admin"
    }
}

# Doctors Database: Key = Doctor ID
# Categorized by Department
doctors_db = {
    "d1": {"id": "d1", "name": "Dr. Rajesh Koothrappali", "department": "Cardiology", "availability": "Mon-Fri, 9am-5pm"},
    "d2": {"id": "d2", "name": "Dr. Priya Sethi", "department": "Dermatology", "availability": "Mon-Sat, 10am-2pm"},
    "d3": {"id": "d3", "name": "Dr. Sanjay Gupta", "department": "General Medicine", "availability": "Tue-Sun, 8am-4pm"},
    "d4": {"id": "d4", "name": "Dr. Anjali Menon", "department": "Pediatrics", "availability": "Mon-Fri, 10am-6pm"},
    "d5": {"id": "d5", "name": "Dr. Sameer Khan", "department": "Orthopedics", "availability": "Wed-Sun, 9am-5pm"}
}

# Appointments: Key = Appointment ID
appointments = {}

# Medical Records: Key = Patient ID
records = {
    "p1": []
}

# Chats: List of message dictionaries
chats = []

def get_user(email):
    return users.get(email)

def get_doctor(doctor_id):
    return doctors_db.get(doctor_id)

def get_all_doctors():
    return list(doctors_db.values())

# Hospitals Database: Indian Mock Data
hospitals_db = {
    "Tamil Nadu": {
        "Chennai": ["Apollo Hospitals", "Fortis Malar", "MIOT International"],
        "Coimbatore": ["Kovai Medical Center", "Ganga Hospital"]
    },
    "Maharashtra": {
        "Mumbai": ["Lilavati Hospital", "Breach Candy", "Nanavati Super Speciality"],
        "Pune": ["Ruby Hall Clinic", "Jehangir Hospital"]
    },
    "Delhi NCR": {
        "New Delhi": ["AIIMS", "Sir Ganga Ram Hospital", "Max Super Speciality"],
        "Gurgaon": ["Medanta - The Medicity", "Artemis Hospital"]
    },
    "Karnataka": {
        "Bangalore": ["Narayana Health", "Manipal Hospital", "Columbia Asia"]
    }
}

# Blood Bank Database
blood_bank_db = {
    "A+": {"group": "A+", "units": 15, "status": "Available"},
    "A-": {"group": "A-", "units": 4, "status": "Low"},
    "B+": {"group": "B+", "units": 22, "status": "Available"},
    "B-": {"group": "B-", "units": 6, "status": "Critical"},
    "O+": {"group": "O+", "units": 30, "status": "Available"},
    "O-": {"group": "O-", "units": 2, "status": "Critical"},
    "AB+": {"group": "AB+", "units": 10, "status": "Available"},
    "AB-": {"group": "AB-", "units": 3, "status": "Low"}
}

# Hospital Capacity Mock
hospital_capacity = {
    "ICU": {"name": "ICU", "total": 20, "occupied": 16, "status": "High Load"},
    "General Ward": {"name": "General Ward", "total": 100, "occupied": 45, "status": "Normal"},
    "Emergency": {"name": "Emergency", "total": 15, "occupied": 5, "status": "Normal"},
    "Operation Theatre": {"name": "Operation Theatre", "total": 8, "occupied": 7, "status": "Critical"}
}

def get_blood_stock():
    return blood_bank_db

def get_hospital_capacity():
    return hospital_capacity

def update_hospital_capacity(ward_name, occupied, status):
    if ward_name in hospital_capacity:
        hospital_capacity[ward_name]['occupied'] = int(occupied)
        hospital_capacity[ward_name]['status'] = status
        return True
    return False

def get_department_load():
    """Calculates active appointments per department"""
    load = {}
    for appt in appointments.values():
        if appt['status'] in ['BOOKED', 'CHECKED-IN', 'CONSULTING']:
            dept = appt.get('doctor_dept', 'General')
            load[dept] = load.get(dept, 0) + 1
    return load

# Blood Donations & Requests
blood_donations = []  # List of {id, donor, group, status, date}
blood_requests = []   # List of {id, doctor_id, group, units, status}

def add_donation(donor_name, group):
    donation = {
        "id": f"don_{len(blood_donations) + 1}",
        "donor": donor_name,
        "group": group,
        "status": "Pending",
        "date": get_formatted_date_time()
    }
    blood_donations.append(donation)
    return donation

def verify_donation(donation_id):
    for don in blood_donations:
        if don['id'] == donation_id and don['status'] == 'Pending':
            don['status'] = 'Verified'
            # Add to stock
            if don['group'] in blood_bank_db:
                blood_bank_db[don['group']]['units'] += 1
            return True
    return False

def get_pending_donations():
    return [d for d in blood_donations if d['status'] == 'Pending']

def request_blood(doctor_id, group, units):
    if group not in blood_bank_db:
        return False
        
    req = {
        "id": f"req_{len(blood_requests) + 1}",
        "doctor_id": doctor_id,
        "group": group,
        "units": units,
        "status": "Requested",
        "date": get_formatted_date_time()
    }
    blood_requests.append(req)
    # Deduct stock immediately for reservation
    if blood_bank_db[group]['units'] >= units:
        blood_bank_db[group]['units'] -= units
        req['status'] = 'Appproved'
        return True, "Approved and Reserved"
    else:
        req['status'] = 'Pending Stock'
        return False, "Not enough stock, request pending"

# Invoices: Key = Invoice ID
invoices = {}

def get_locations():
    return hospitals_db

# --- Timezone Helper (IST) ---
import datetime
import pytz

def get_ist_time():
    """Returns current time in Indian Standard Time (IST)."""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist)

def get_formatted_date_time():
    """Returns formatted date string DD-MM-YYYY HH:MM AM/PM"""
    return get_ist_time().strftime("%d-%m-%Y %I:%M %p")

# --- Chat Functions ---
def add_chat_message(sender_name, department, message, sender_role='patient'):
    chat_id = len(chats) + 1
    new_msg = {
        'id': chat_id,
        'sender': sender_name,
        'role': sender_role,
        'dept': department,
        'message': message,
        'time': get_formatted_date_time(),
        'reply': None
    }
    chats.append(new_msg)
    return new_msg

def get_chat_messages(department=None):
    if department:
        # Filter by department for doctors/viewing specific channels
        return [msg for msg in chats if msg['dept'] == department]
    return chats

def request_doctor_reply(chat_id, reply_text):
    for msg in chats:
        if msg['id'] == int(chat_id):
            msg['reply'] = reply_text
            return True
    return False

# --- Core Functions ---

def create_appointment(patient_id, doctor_id, time, center=None, state=None):
    appt_id = f"appt_{len(appointments) + 1}"
    
    # Auto-generate an invoice in INR
    invoice_amount = 500  # ₹500 Consultation Fee
    inv_id = f"inv_{len(invoices) + 1}"
    
    # Format time if possible, otherwise use input
    try:
        # If input is ISO layout, try to format. This is tricky with HTML inputs.
        # Let's just keep strict string for now or formatted
        date_str = time.replace("T", " ")
    except:
        date_str = time

    invoices[inv_id] = {
        "id": inv_id,
        "appt_id": appt_id,
        "patient_id": patient_id,
        "amount": invoice_amount,
        "status": "Unpaid", 
        "date": get_formatted_date_time().split(" ")[0], 
        "details": f"Consultation Fee - {center if center else 'General'}"
    }

    appointments[appt_id] = {
        "id": appt_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "doctor_name": doctors_db[doctor_id]["name"],
        "doctor_dept": doctors_db[doctor_id]["department"],
        "time": date_str,
        "location": f"{center}, {state}" if center else "Main Clinic",
        "status": "BOOKED", 
        "review": None,
        "invoice_id": inv_id
    }
    return appointments[appt_id]

def get_patient_invoices(patient_id):
    return [inv for inv in invoices.values() if inv["patient_id"] == patient_id]

def update_invoice_status(inv_id, status):
    if inv_id in invoices:
        invoices[inv_id]["status"] = status
        return True
    return False

def get_appointments_by_patient(patient_id):
    return [appt for appt in appointments.values() if appt["patient_id"] == patient_id]

def get_appointments_by_doctor(doctor_id):
    return [appt for appt in appointments.values() if appt["doctor_id"] == doctor_id]

def update_appointment_status(appt_id, new_status):
    if appt_id in appointments:
        appointments[appt_id]["status"] = new_status
        return True
    return False

def add_record(patient_id, filename, ai_summary):
    if patient_id not in records:
        records[patient_id] = []
    
    record_id = f"rec_{len(records[patient_id]) + 1}"
    new_record = {
        "id": record_id,
        "filename": filename,
        "ai_summary": ai_summary,
        "date": get_formatted_date_time()
    }
    records[patient_id].append(new_record)
    return new_record

def get_patient_records(patient_id):
    return records.get(patient_id, [])

def get_all_patients():
    """Returns a list of all users with role 'patient'."""
    return [user for user in users.values() if user['role'] == 'patient']

def get_weekly_stats(doctor_id):
    # Simulated data
    return [
        {"day": "Mon", "count": 12},
        {"day": "Tue", "count": 19},
        {"day": "Wed", "count": 15},
        {"day": "Thu", "count": 22},
        {"day": "Fri", "count": 18},
        {"day": "Sat", "count": 8},
        {"day": "Sun", "count": 5}
    ]

# Appointments: Key = Appointment ID
appointments = {}

# Medical Records: Key = Patient ID (Values are lists of records)
records = {
    "p1": []
}

# Mood Logs: Key = Patient ID (Values = List of {date, score, note})
mood_logs = {
    "p1": [] 
}

def log_mood(patient_id, score, note):
    if patient_id not in mood_logs:
        mood_logs[patient_id] = []
        
    import datetime
    entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.datetime.now().strftime("%H:%M"),
        "score": int(score), # 1-5
        "note": note
    }
    mood_logs[patient_id].append(entry)
    return entry

def get_mood_history(patient_id):
    return mood_logs.get(patient_id, [])

def get_user(email):
    return users.get(email)

def get_doctor(doctor_id):
    return doctors_db.get(doctor_id)

def get_all_doctors():
    return list(doctors_db.values())

# Hospitals Database: Mock Data for Location Selection
hospitals_db = {
    "New York": {
        "Manhattan": ["City Health Center", "Metro General", "Downtown Clinic"],
        "Brooklyn": ["Brooklyn Heights Medical", "Kings County Care"]
    },
    "California": {
        "Los Angeles": ["LA General", "Sunset Boulevard Clinic"],
        "San Francisco": ["Bay Area Medical", "Golden Gate Health"]
    },
    "Texas": {
        "Houston": ["Houston Medical Center", "Space City Care"],
        "Austin": ["Capital Health", "River City Clinic"]
    }
}

# Invoices: Key = Invoice ID
invoices = {}

def get_locations():
    return hospitals_db

def create_appointment(patient_id, doctor_id, time, center=None, state=None, age=None, gender=None, reason=None):
    appt_id = f"appt_{len(appointments) + 1}"
    
    # Auto-generate an invoice for the appointment
    invoice_amount = 150 # Mock standard consultation fee
    inv_id = f"inv_{len(invoices) + 1}"
    
    invoices[inv_id] = {
        "id": inv_id,
        "appt_id": appt_id,
        "patient_id": patient_id,
        "amount": invoice_amount,
        "status": "Unpaid", # Unpaid, Paid, Claimed
        "date": time.split("T")[0] if "T" in time else time,
        "details": f"Consultation Fee - {center if center else 'General'}"
    }

    appointments[appt_id] = {
        "id": appt_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "doctor_name": doctors_db[doctor_id]["name"],
        "time": time,
        "location": f"{center}, {state}" if center else "Main Clinic",
        "status": "BOOKED", 
        "review": None,
        "invoice_id": inv_id,
        "age": age,
        "gender": gender,
        "reason": reason
    }
    return appointments[appt_id]

def get_patient_invoices(patient_id):
    return [inv for inv in invoices.values() if inv["patient_id"] == patient_id]

def update_invoice_status(inv_id, status):
    if inv_id in invoices:
        invoices[inv_id]["status"] = status
        return True
    return False

def get_appointments_by_patient(patient_id):
    return [appt for appt in appointments.values() if appt["patient_id"] == patient_id]

def get_appointments_by_doctor(doctor_id):
    return [appt for appt in appointments.values() if appt["doctor_id"] == doctor_id]

def update_appointment_status(appt_id, new_status):
    if appt_id in appointments:
        appointments[appt_id]["status"] = new_status
        return True
    return False

def add_record(patient_id, filename, ai_summary, category='Report'):
    if patient_id not in records:
        records[patient_id] = []
    
    import datetime
    record_id = f"rec_{len(records[patient_id]) + 1}"
    new_record = {
        "id": record_id,
        "filename": filename,
        "ai_summary": ai_summary,
        "category": category,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    records[patient_id].append(new_record)
    return new_record

def get_patient_records(patient_id):
    return records.get(patient_id, [])

def get_all_patients():
    """Returns a list of all users with role 'patient'."""
    return [user for user in users.values() if user['role'] == 'patient']

def get_weekly_stats(doctor_id):
    """
    Returns simulated daily patient counts for the last 7 days.
    In a real app, this would query appointments by date.
    """
    return [
        {"day": "Mon", "count": 12},
        {"day": "Tue", "count": 19},
        {"day": "Wed", "count": 15},
        {"day": "Thu", "count": 22},
        {"day": "Fri", "count": 18},
        {"day": "Sat", "count": 8},
        {"day": "Sun", "count": 5}
    ]
