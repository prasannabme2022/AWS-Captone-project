from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
import boto3
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv
from decimal import Decimal
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'medtrack-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'ap-south-1')
PATIENTS_TABLE = 'medtrack_patients'
DOCTORS_TABLE = 'medtrack_doctors'
APPOINTMENTS_TABLE = 'medtrack_appointments'
MEDICAL_VAULT_TABLE = 'medtrack_medical_vault'
BLOOD_BANK_TABLE = 'medtrack_blood_bank'
INVOICES_TABLE = 'medtrack_invoices'
CHAT_MESSAGES_TABLE = 'medtrack_chat_messages'
MOOD_LOGS_TABLE = 'medtrack_mood_logs'
SNS_TOPIC_ARN = os.getenv('arn:aws:sns:ap-southeast-2:050690756868:Medtrack_cloud_enabled_healthcare_management')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AWS clients
try:
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    sns_client = boto3.client('sns', region_name=AWS_REGION)
    
    # Table configurations
    TABLES_CONFIG = [
        {'name': PATIENTS_TABLE, 'key': 'email'},
        {'name': DOCTORS_TABLE, 'key': 'email'},
        {'name': APPOINTMENTS_TABLE, 'key': 'appointment_id'},
        {'name': MEDICAL_VAULT_TABLE, 'key': 'vault_id'},
        {'name': BLOOD_BANK_TABLE, 'key': 'blood_group'},
        {'name': INVOICES_TABLE, 'key': 'invoice_id'},
        {'name': CHAT_MESSAGES_TABLE, 'key': 'message_id'},
        {'name': MOOD_LOGS_TABLE, 'key': 'mood_id'}
    ]

    def create_tables():
        """Create DynamoDB tables if they don't exist"""
        existing_tables = [t.name for t in dynamodb.tables.all()]
        
        for table_config in TABLES_CONFIG:
            table_name = table_config['name']
            key_name = table_config['key']
            
            if table_name not in existing_tables:
                logger.info(f"Creating table: {table_name}")
                try:
                    dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=[{'AttributeName': key_name, 'KeyType': 'HASH'}],
                        AttributeDefinitions=[{'AttributeName': key_name, 'AttributeType': 'S'}],
                        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    )
                    logger.info(f"Table {table_name} creation initiated.")
                except ClientError as e:
                    logger.error(f"Failed to create table {table_name}: {e}")
            else:
                logger.info(f"Table {table_name} already exists.")

    # Initialize all DynamoDB tables (lazy reference)
    patients_table = dynamodb.Table(PATIENTS_TABLE)
    doctors_table = dynamodb.Table(DOCTORS_TABLE)
    appointments_table = dynamodb.Table(APPOINTMENTS_TABLE)
    medical_vault_table = dynamodb.Table(MEDICAL_VAULT_TABLE)
    blood_bank_table = dynamodb.Table(BLOOD_BANK_TABLE)
    invoices_table = dynamodb.Table(INVOICES_TABLE)
    chat_messages_table = dynamodb.Table(CHAT_MESSAGES_TABLE)
    mood_logs_table = dynamodb.Table(MOOD_LOGS_TABLE)
    
    logger.info("AWS services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AWS services: {e}")
    # Continue execution for local testing handling or graceful failure
    pass

# ============================================
# HELPER FUNCTIONS
# ============================================

def to_decimal(value):
    """Convert float to Decimal for DynamoDB storage"""
    if isinstance(value, float):
        return Decimal(str(value))
    return value

def serialize_datetime(obj):
    """Serialize datetime and Decimal objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def deserialize_item(item):
    """Deserialize DynamoDB item to Python dict"""
    if not item:
        return None
    result = {}
    for key, value in item.items():
        if isinstance(value, str) and 'T' in value:
            try:
                result[key] = datetime.fromisoformat(value)
            except ValueError:
                result[key] = value
        elif isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result

def generate_id(prefix=""):
    """Generate unique ID with optional prefix"""
    return prefix + str(uuid.uuid4().hex)[:8]

def get_current_datetime():
    """Get current datetime as ISO string"""
    return datetime.now().isoformat()

# ============================================
# SNS NOTIFICATION SERVICE
# ============================================

def send_notification(message, subject="MedTrack Notification"):
    """Send SNS notification"""
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        logger.info(f"SNS notification sent: {response['MessageId']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SNS notification: {e}")
        return False

# ============================================
# PATIENT MANAGEMENT
# ============================================

def get_patient(email):
    """Get patient by email from DynamoDB"""
    try:
        response = patients_table.get_item(Key={'email': email})
        return deserialize_item(response.get('Item'))
    except ClientError as e:
        logger.error(f"Error getting patient {email}: {e}")
        return None

def create_patient(email, password, name, phone, address, dob, blood_group):
    """Create patient in DynamoDB"""
    try:
        if not password or not isinstance(password, str) or len(password.strip()) == 0:
            logger.error("Invalid password provided")
            return False
        
        patient_data = {
            'email': email,
            'password': generate_password_hash(password.strip(), method='pbkdf2:sha256'),
            'name': name,
            'phone': phone or '',
            'address': address or '',
            'dob': dob or '',
            'blood_group': blood_group or '',
            'role': 'patient',
            'created_at': get_current_datetime(),
            'mood_history': []
        }
        
        patients_table.put_item(
            Item=patient_data,
            ConditionExpression='attribute_not_exists(email)'
        )
        
        # Send notification
        send_notification(
            f"New patient registered: {name} ({email})",
            "New Patient Registration"
        )
        
        logger.info(f"Patient created successfully: {email}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.warning(f"Patient already exists: {email}")
            return False
        logger.error(f"Error creating patient {email}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating patient {email}: {e}")
        return False

def update_patient(email, updates):
    """Update patient information"""
    try:
        update_expr = "SET "
        expr_values = {}
        expr_names = {}
        
        for idx, (key, value) in enumerate(updates.items()):
            attr_name = f"#attr{idx}"
            attr_value = f":val{idx}"
            update_expr += f"{attr_name} = {attr_value}, "
            expr_names[attr_name] = key
            expr_values[attr_value] = value
        
        update_expr = update_expr.rstrip(', ')
        
        patients_table.update_item(
            Key={'email': email},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )
        
        logger.info(f"Patient updated: {email}")
        return True
    except ClientError as e:
        logger.error(f"Error updating patient {email}: {e}")
        return False

# ============================================
# DOCTOR MANAGEMENT
# ============================================

def get_doctor(email):
    """Get doctor by email from DynamoDB"""
    try:
        response = doctors_table.get_item(Key={'email': email})
        return deserialize_item(response.get('Item'))
    except ClientError as e:
        logger.error(f"Error getting doctor {email}: {e}")
        return None

def create_doctor(email, password, name, phone, specialization, license_number):
    """Create doctor in DynamoDB"""
    try:
        if not password or not isinstance(password, str) or len(password.strip()) == 0:
            logger.error("Invalid password provided")
            return False
        
        doctor_data = {
            'email': email,
            'password': generate_password_hash(password.strip(), method='pbkdf2:sha256'),
            'name': name,
            'phone': phone or '',
            'specialization': specialization or '',
            'license_number': license_number or '',
            'role': 'doctor',
            'status': 'available',
            'created_at': get_current_datetime()
        }
        
        doctors_table.put_item(
            Item=doctor_data,
            ConditionExpression='attribute_not_exists(email)'
        )
        
        # Send notification
        send_notification(
            f"New doctor registered: Dr. {name} ({specialization})",
            "New Doctor Registration"
        )
        
        logger.info(f"Doctor created successfully: {email}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.warning(f"Doctor already exists: {email}")
            return False
        logger.error(f"Error creating doctor {email}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating doctor {email}: {e}")
        return False

def get_all_doctors():
    """Get all doctors from DynamoDB"""
    try:
        response = doctors_table.scan()
        doctors = [deserialize_item(item) for item in response.get('Items', [])]
        return doctors
    except ClientError as e:
        logger.error(f"Error getting all doctors: {e}")
        return []

# ============================================
# APPOINTMENT MANAGEMENT
# ============================================

def create_appointment(patient_email, doctor_email, appointment_date, symptoms, priority='normal'):
    """Create appointment in DynamoDB"""
    try:
        appointment_id = generate_id("APPT")
        
        appointment_data = {
            'appointment_id': appointment_id,
            'patient_email': patient_email,
            'doctor_email': doctor_email,
            'appointment_date': appointment_date,
            'symptoms': symptoms or '',
            'priority': priority,
            'status': 'BOOKED',
            'diagnosis': '',
            'prescription': '',
            'created_at': get_current_datetime(),
            'updated_at': get_current_datetime()
        }
        
        appointments_table.put_item(Item=appointment_data)
        
        # Get patient and doctor names safely
        patient = get_patient(patient_email)
        doctor = get_doctor(doctor_email)
        
        patient_name = patient.get('name', patient_email) if patient else patient_email
        doctor_name = doctor.get('name', doctor_email) if doctor else doctor_email
        
        # Send notification
        send_notification(
            f"New appointment booked by {patient_name} with Dr. {doctor_name} on {appointment_date}",
            "New Appointment Booked"
        )
        
        logger.info(f"Appointment created: {appointment_id}")
        return appointment_id
    except ClientError as e:
        logger.error(f"Error creating appointment: {e}")
        return None

def get_appointment(appointment_id):
    """Get appointment by ID"""
    try:
        response = appointments_table.get_item(Key={'appointment_id': appointment_id})
        return deserialize_item(response.get('Item'))
    except ClientError as e:
        logger.error(f"Error getting appointment {appointment_id}: {e}")
        return None

def update_appointment_status(appointment_id, status, diagnosis='', prescription=''):
    """Update appointment status and details"""
    try:
        update_data = {
            'status': status,
            'updated_at': get_current_datetime()
        }
        
        if diagnosis:
            update_data['diagnosis'] = diagnosis
        if prescription:
            update_data['prescription'] = prescription
        
        update_expr = "SET "
        expr_values = {}
        for key, value in update_data.items():
            update_expr += f"{key} = :{key}, "
            expr_values[f":{key}"] = value
        update_expr = update_expr.rstrip(', ')
        
        appointments_table.update_item(
            Key={'appointment_id': appointment_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )
        
        # Send notification
        appointment = get_appointment(appointment_id)
        send_notification(
            f"Appointment {appointment_id} status updated to: {status}",
            "Appointment Status Update"
        )
        
        logger.info(f"Appointment updated: {appointment_id}")
        return True
    except ClientError as e:
        logger.error(f"Error updating appointment {appointment_id}: {e}")
        return False

def get_patient_appointments(patient_email):
    """Get all appointments for a patient"""
    try:
        response = appointments_table.scan(
            FilterExpression='patient_email = :email',
            ExpressionAttributeValues={':email': patient_email}
        )
        appointments = [deserialize_item(item) for item in response.get('Items', [])]
        
        # Enrich appointments with details for display
        for appt in appointments:
            # Map time
            # Map time
            date_val = appt.get('appointment_date')
            appt['time'] = str(date_val).replace('T', ' ') if date_val else 'N/A'
            
            # Get Doctor Name
            if 'doctor_email' in appt:
                doc = get_doctor(appt['doctor_email'])
                appt['doctor_name'] = doc.get('name', appt['doctor_email']) if doc else appt['doctor_email']
            else:
                 appt['doctor_name'] = 'Unknown Doctor'
                 
        return sorted(appointments, key=lambda x: x.get('created_at', ''), reverse=True)
    except ClientError as e:
        logger.error(f"Error getting patient appointments: {e}")
        return []

def get_doctor_appointments(doctor_email):
    """Get all appointments for a doctor"""
    try:
        response = appointments_table.scan(
            FilterExpression='doctor_email = :email',
            ExpressionAttributeValues={':email': doctor_email}
        )
        appointments = [deserialize_item(item) for item in response.get('Items', [])]
        return sorted(appointments, key=lambda x: x.get('created_at', ''), reverse=True)
    except ClientError as e:
        logger.error(f"Error getting doctor appointments: {e}")
        return []

# ============================================
# MEDICAL VAULT (FILE STORAGE)
# ============================================

def add_to_medical_vault(patient_email, file_name, file_type, file_path, analysis=''):
    """Add medical file to vault"""
    try:
        vault_id = generate_id("VAULT")
        
        vault_data = {
            'vault_id': vault_id,
            'patient_email': patient_email,
            'file_name': file_name,
            'file_type': file_type,
            'file_path': file_path,
            'analysis': analysis or '',
            'uploaded_at': get_current_datetime()
        }
        
        medical_vault_table.put_item(Item=vault_data)
        
        logger.info(f"Medical file added to vault: {vault_id} for patient {patient_email}")
        return vault_id
    except ClientError as e:
        logger.error(f"Error adding to medical vault: {e}")
        return None

def get_patient_vault(patient_email):
    """Get all medical files for a patient"""
    try:
        response = medical_vault_table.scan(
            FilterExpression='patient_email = :email',
            ExpressionAttributeValues={':email': patient_email}
        )
        vault_items = [deserialize_item(item) for item in response.get('Items', [])]
        return sorted(vault_items, key=lambda x: x.get('uploaded_at', ''), reverse=True)
    except ClientError as e:
        logger.error(f"Error getting patient vault: {e}")
        return []

# ============================================
# BLOOD BANK MANAGEMENT
# ============================================

def get_blood_stock():
    """Get current blood stock for all blood groups"""
    try:
        response = blood_bank_table.scan()
        blood_stock = {}
        for item in response.get('Items', []):
            blood_group = item.get('blood_group')
            units = int(item.get('units', 0))
            blood_stock[blood_group] = units
        
        # Ensure all blood groups exist
        all_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        for group in all_groups:
            if group not in blood_stock:
                blood_stock[group] = 0
        
        return blood_stock
    except ClientError as e:
        logger.error(f"Error getting blood stock: {e}")
        return {}

def update_blood_stock(blood_group, units):
    """Update blood stock for a blood group"""
    try:
        blood_bank_table.put_item(
            Item={
                'blood_group': blood_group,
                'units': int(units),
                'updated_at': get_current_datetime()
            }
        )
        
        logger.info(f"Blood stock updated: {blood_group} = {units} units")
        return True
    except ClientError as e:
        logger.error(f"Error updating blood stock: {e}")
        return False

# ============================================
# INVOICE & INSURANCE MANAGEMENT
# ============================================

def create_invoice(patient_email, appointment_id, amount, description):
    """Create invoice for patient"""
    try:
        invoice_id = generate_id("INV")
        
        invoice_data = {
            'invoice_id': invoice_id,
            'patient_email': patient_email,
            'appointment_id': appointment_id,
            'amount': to_decimal(amount),
            'description': description,
            'status': 'unpaid',
            'insurance_claimed': False,
            'created_at': get_current_datetime()
        }
        
        invoices_table.put_item(Item=invoice_data)
        
        # Send notification
        send_notification(
            f"New invoice generated for patient {patient_email}: ₹{amount}",
            "New Invoice"
        )
        
        logger.info(f"Invoice created: {invoice_id}")
        return invoice_id
    except ClientError as e:
        logger.error(f"Error creating invoice: {e}")
        return None

def get_patient_invoices(patient_email):
    """Get all invoices for a patient"""
    try:
        response = invoices_table.scan(
            FilterExpression='patient_email = :email',
            ExpressionAttributeValues={':email': patient_email}
        )
        invoices = [deserialize_item(item) for item in response.get('Items', [])]
        return sorted(invoices, key=lambda x: x.get('created_at', ''), reverse=True)
    except ClientError as e:
        logger.error(f"Error getting patient invoices: {e}")
        return []

def claim_insurance(invoice_id):
    """Claim insurance for an invoice"""
    try:
        invoices_table.update_item(
            Key={'invoice_id': invoice_id},
            UpdateExpression="SET insurance_claimed = :claimed, updated_at = :updated",
            ExpressionAttributeValues={
                ':claimed': True,
                ':updated': get_current_datetime()
            }
        )
        
        # Send notification
        send_notification(
            f"Insurance claim submitted for invoice {invoice_id}",
            "Insurance Claim"
        )
        
        logger.info(f"Insurance claimed for invoice: {invoice_id}")
        return True
    except ClientError as e:
        logger.error(f"Error claiming insurance: {e}")
        return False

# ============================================
# CHAT & MESSAGING
# ============================================

def send_chat_message(sender_email, receiver_email, message, sender_type='patient'):
    """Send chat message between patient and doctor"""
    try:
        message_id = generate_id("MSG")
        
        message_data = {
            'message_id': message_id,
            'sender_email': sender_email,
            'receiver_email': receiver_email,
            'message': message,
            'sender_type': sender_type,
            'read': False,
            'created_at': get_current_datetime()
        }
        
        chat_messages_table.put_item(Item=message_data)
        
        logger.info(f"Chat message sent: {message_id}")
        return message_id
    except ClientError as e:
        logger.error(f"Error sending chat message: {e}")
        return None

def get_chat_messages(user1_email, user2_email):
    """Get all chat messages between two users"""
    try:
        response = chat_messages_table.scan()
        all_messages = [deserialize_item(item) for item in response.get('Items', [])]
        
        # Filter messages between the two users
        chat_messages = [
            msg for msg in all_messages
            if (msg.get('sender_email') == user1_email and msg.get('receiver_email') == user2_email) or
               (msg.get('sender_email') == user2_email and msg.get('receiver_email') == user1_email)
        ]
        
        return sorted(chat_messages, key=lambda x: x.get('created_at', ''))
    except ClientError as e:
        logger.error(f"Error getting chat messages: {e}")
        return []

# ============================================
# MOOD TRACKING
# ============================================

def log_mood(patient_email, mood, notes=''):
    """Log mood for a patient"""
    try:
        mood_id = generate_id("MOOD")
        
        mood_data = {
            'mood_id': mood_id,
            'patient_email': patient_email,
            'mood': mood,
            'notes': notes,
            'logged_at': get_current_datetime()
        }
        
        mood_logs_table.put_item(Item=mood_data)
        
        logger.info(f"Mood logged: {mood_id} for patient {patient_email}")
        return mood_id
    except ClientError as e:
        logger.error(f"Error logging mood: {e}")
        return None

def get_mood_history(patient_email):
    """Get mood history for a patient"""
    try:
        response = mood_logs_table.scan(
            FilterExpression='patient_email = :email',
            ExpressionAttributeValues={':email': patient_email}
        )
        mood_logs = [deserialize_item(item) for item in response.get('Items', [])]
        return sorted(mood_logs, key=lambda x: x.get('logged_at', ''), reverse=True)
    except ClientError as e:
        logger.error(f"Error getting mood history: {e}")
        return []

# ============================================
# AI CHATBOT HELPERS
# ============================================

def get_chatbot_response(patient_email, message):
    """
    AI Chatbot response generator
    This is a placeholder - integrate with your ML model or external AI API
    """
    # Simple rule-based responses (replace with actual AI model)
    message_lower = message.lower()
    
    responses = {
        'fever': "I understand you have a fever. Please monitor your temperature. If it exceeds 102°F or persists for more than 3 days, consult a doctor immediately.",
        'headache': "For headache, ensure you're well-hydrated and rested. If severe or persistent, please book an appointment with a doctor.",
        'appointment': "You can book an appointment from the patient dashboard. Select your preferred doctor and date.",
        'blood': "You can check blood bank availability in the Blood Bank section. We maintain stock of all blood groups.",
        'help': "I'm here to help! You can ask me about symptoms, appointments, blood bank, or general health queries."
    }
    
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    return "I'm here to assist you. Please describe your symptoms or ask any health-related questions."

# ============================================
# FLASK ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            name = data.get('name', '').strip()
            phone = data.get('phone', '').strip()
            role = data.get('role', '').strip()
            
            # Validate inputs
            if not all([email, password, name, role]):
                flash('All fields are required.', 'error')
                return render_template('signup.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('signup.html')
            
            # Check if user already exists
            if get_patient(email) or get_doctor(email):
                flash('Email already exists. Please choose a different one.', 'error')
                return render_template('signup.html')
            
            # Create user based on role
            success = False
            if role == 'patient':
                dob = data.get('dob', '')
                blood_group = data.get('blood_group', '')
                address = data.get('address', '').strip()
                success = create_patient(email, password, name, phone, address, dob, blood_group)
            elif role == 'doctor':
                specialization = data.get('specialization', '').strip()
                license_number = data.get('license_number', '').strip()
                success = create_doctor(email, password, name, phone, specialization, license_number)
            
            if success:
                flash('Account created successfully! Please sign in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Failed to create account. Please try again.', 'error')
                
        except Exception as e:
            logger.error(f"Signup error: {e}")
            flash('An error occurred during signup. Please try again.', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            
            if not email or not password:
                flash('Please enter both email and password.', 'error')
                return render_template('login.html')
            
            # Check explicit admin credentials (hardcoded for demo)
            if email == 'admin@medtrack.com' and password == 'admin123':
                session['user_id'] = 'admin'
                session['role'] = 'admin'
                session['name'] = 'Administrator'
                flash('Welcome, Administrator!', 'success')
                return redirect(url_for('admin_dashboard'))

            # Check in patients table
            patient = get_patient(email)
            print(f"DEBUG: Retrieved patient for {email}: {patient}")
            if patient:
                print(f"DEBUG: Stored hash: {patient.get('password')}, Input password: {password}")
                is_valid = check_password_hash(patient['password'], password)
                print(f"DEBUG: Password match: {is_valid}")
                if is_valid:
                    session['user_id'] = email
                    session['role'] = 'patient'
                    session['name'] = patient['name']
                    
                    flash(f"Welcome back, {patient['name']}!", 'success')
                    return redirect(url_for('patient_dashboard'))
            
            # Check in doctors table
            doctor = get_doctor(email)
            print(f"DEBUG: Retrieved doctor for {email}: {doctor}")
            if doctor:
                print(f"DEBUG: Stored hash: {doctor.get('password')}, Input password: {password}")
                is_valid = check_password_hash(doctor['password'], password)
                print(f"DEBUG: Password match: {is_valid}")
                if is_valid:
                    session['user_id'] = email
                    session['role'] = 'doctor'
                    session['name'] = doctor['name']
                    
                    flash(f"Welcome back, Dr. {doctor['name']}!", 'success')
                    return redirect(url_for('doctor_dashboard'))
            
            flash('Invalid email or password.', 'error')
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('An error occurred during login. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/login')
def admin_login():
    flash("Please log in with Administrator credentials.", "info")
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Please login as admin first.', 'error')
        return redirect(url_for('login'))
    
    # Simple stats for the dashboard
    stats = {
        'doctors': len(get_all_doctors()),
        'patients': 0, # get_all_patients not implemented cheaply, skip for now or implement
        'appointments': 0,
        'departments': 4
    }
    
    # We can try to scan if we want accurate numbers, but for speed just render template
    # Re-using the existing admin dashboard template but passing necessary variables
    # The existing template expects 'stats', 'patients', 'blood_stock' etc.
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         patients=[],
                         blood_stock=get_blood_stock(),
                         capacity={'ICU': {'status': 'Normal', 'occupied': 8, 'total': 12}, 
                                   'General Ward': {'status': 'Normal', 'occupied': 45, 'total': 60}},
                         dept_load={'Cardiology': 20},
                         pending_donations=[])

@app.route('/admin/doctors')
def admin_doctors():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    doctors = get_all_doctors()
    return render_template('admin/doctors_list.html', doctors=doctors)

@app.route('/admin/patients')
def admin_patients():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('admin/patients_list.html', patients=[])

@app.route('/admin/appointments')
def admin_appointments():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('admin/appointments_list.html', appointments=[])

@app.route('/admin/records')
def admin_records():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('admin/records_list.html', item_counts={})

@app.route('/admin/invoices')
def admin_invoices():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('admin/invoices_list.html', invoices=[])

@app.route('/patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session or session.get('role') != 'patient':
        flash('Please login as a patient first.', 'info')
        return redirect(url_for('login'))
    
    appointments = get_patient_appointments(session['user_id'])
    return render_template('patient/dashboard.html', appointments=appointments)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session.get('role') != 'doctor':
        flash('Please login as a doctor first.', 'info')
        return redirect(url_for('login'))
    
    appointments = get_doctor_appointments(session['user_id'])
    
    # Calculate stats
    total_patients = len(set(a['patient_id'] for a in appointments))
    today_appointments = [a for a in appointments if a.get('date') == datetime.now().strftime('%Y-%m-%d')] # Basic check, might need better date parsing
    
    stats = {
        'total_patients': total_patients,
        'today_patients': len(today_appointments),
        'today_appts': len(today_appointments)
    }
    
    # Mock alerts and next_patient for demo if list is empty
    next_patient = None
    if appointments:
        # Just pick the first as next for demo
        first_ppt = appointments[0]
        next_patient = {
            'name': first_ppt['patient_id'], # Using ID as name if name not available in appointment
            'id': first_ppt['patient_id'],
            'dob': '1990-01-01'
        }
        
    return render_template('doctor/dashboard.html', 
                         appointments=appointments,
                         stats=stats,
                         today_appointments=today_appointments,
                         next_patient=next_patient,
                         now_date=datetime.now().strftime('%d %b, %Y'),
                         alerts=[{'group': 'O-', 'units': 2}])

@app.route('/doctor/patients')
def doctor_patients_list():
    if session.get('role') != 'doctor': return redirect(url_for('login'))
    # In a real app we would filter by doctor, but for this demo showing all is acceptable or empty list
    return render_template('doctor/patients_list.html', patients=[])

@app.route('/doctor/appointments')
def doctor_appointments_list():
    if session.get('role') != 'doctor': return redirect(url_for('login'))
    appointments = get_doctor_appointments(session['user_id'])
    return render_template('doctor/appointments_list.html', appointments=appointments)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session or session.get('role') != 'patient':
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        doctor_email = request.form.get('doctor_email')
        appointment_date = request.form.get('appointment_date')
        symptoms = request.form.get('symptoms')
        
        appointment_id = create_appointment(
            session['user_id'], 
            doctor_email, 
            appointment_date, 
            symptoms
        )
        
        if appointment_id:
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Error booking appointment.', 'error')
    
    
    # Mock Locations for the dropdown
    locations = {
        'Andhra Pradesh': {'Visakhapatnam': ['MedTrack Vizag'], 'Vijayawada': ['MedTrack Vijayawada']},
        'Arunachal Pradesh': {'Itanagar': ['MedTrack Itanagar']},
        'Assam': {'Guwahati': ['MedTrack Guwahati']},
        'Bihar': {'Patna': ['MedTrack Patna']},
        'Chhattisgarh': {'Raipur': ['MedTrack Raipur']},
        'Goa': {'Panaji': ['MedTrack Panaji']},
        'Gujarat': {'Ahmedabad': ['MedTrack Ahmedabad', 'MedTrack Gandhi Nagar'], 'Surat': ['MedTrack Surat']},
        'Haryana': {'Gurugram': ['MedTrack Cyber City'], 'Faridabad': ['MedTrack Faridabad']},
        'Himachal Pradesh': {'Shimla': ['MedTrack Shimla']},
        'Jharkhand': {'Ranchi': ['MedTrack Ranchi']},
        'Karnataka': {'Bangalore': ['MedTrack Tech Park', 'MedTrack City'], 'Mysore': ['MedTrack Mysore']},
        'Kerala': {'Kochi': ['MedTrack Kochi'], 'Thiruvananthapuram': ['MedTrack Trivandrum']},
        'Madhya Pradesh': {'Bhopal': ['MedTrack Bhopal'], 'Indore': ['MedTrack Indore']},
        'Maharashtra': {'Mumbai': ['MedTrack Central', 'MedTrack South'], 'Pune': ['MedTrack Pune Core'], 'Nagpur': ['MedTrack Nagpur']},
        'Manipur': {'Imphal': ['MedTrack Imphal']},
        'Meghalaya': {'Shillong': ['MedTrack Shillong']},
        'Mizoram': {'Aizawl': ['MedTrack Aizawl']},
        'Nagaland': {'Kohima': ['MedTrack Kohima']},
        'Odisha': {'Bhubaneswar': ['MedTrack Bhubaneswar']},
        'Punjab': {'Chandigarh': ['MedTrack Chandigarh'], 'Ludhiana': ['MedTrack Ludhiana']},
        'Rajasthan': {'Jaipur': ['MedTrack Jaipur'], 'Udaipur': ['MedTrack Udaipur']},
        'Sikkim': {'Gangtok': ['MedTrack Gangtok']},
        'Tamil Nadu': {'Chennai': ['MedTrack Chennai', 'MedTrack OMR'], 'Coimbatore': ['MedTrack Coimbatore']},
        'Telangana': {'Hyderabad': ['MedTrack HITEC', 'MedTrack Secunderabad']},
        'Tripura': {'Agartala': ['MedTrack Agartala']},
        'Uttar Pradesh': {'Lucknow': ['MedTrack Lucknow'], 'Noida': ['MedTrack Noida'], 'Varanasi': ['MedTrack Varanasi']},
        'Uttarakhand': {'Dehradun': ['MedTrack Dehradun']},
        'West Bengal': {'Kolkata': ['MedTrack Kolkata', 'MedTrack Salt Lake']},
        'Delhi': {'New Delhi': ['MedTrack AIIMS Link', 'MedTrack North']},
        'Jammu and Kashmir': {'Srinagar': ['MedTrack Srinagar']},
        'Ladakh': {'Leh': ['MedTrack Leh']},
        'Puducherry': {'Puducherry': ['MedTrack Pondicherry']},
        'Andaman and Nicobar Islands': {'Port Blair': ['MedTrack Port Blair']},
        'Chandigarh': {'Chandigarh': ['MedTrack Chandigarh City']},
        'Dadra and Nagar Haveli and Daman and Diu': {'Daman': ['MedTrack Daman']},
        'Lakshadweep': {'Kavaratti': ['MedTrack Kavaratti']}
    }

    doctors = get_all_doctors()
    # Normalize doctors for the template JS (ensure department key exists)
    for d in doctors:
        d['department'] = d.get('specialization', 'General')
        d['availability'] = d.get('status', 'Available')

    return render_template('patient/book.html', doctors=doctors, locations=locations)

@app.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '')
        
        # Get AI response
        response = get_chatbot_response(session['user_id'], message)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    return render_template('patient/assistant.html')

@app.route('/patient_assistant')
def patient_assistant():
    return redirect(url_for('ai_chat'))

@app.route('/patient_chat')
def patient_chat():
    if 'user_id' not in session or session.get('role') != 'patient':
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    # In a real app we'd load chat history here
    return render_template('patient/chat.html', recent_doctors=[])

@app.route('/doctor/chat')
def doctor_chat_view():
    if session.get('role') != 'doctor': return redirect(url_for('login'))
    return render_template('doctor/chat.html', recent_patients=[])

@app.route('/patient_vault')
def patient_vault():
    if 'user_id' not in session or session.get('role') != 'patient':
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    vault_items = get_patient_vault(session['user_id'])
    return render_template('patient/vault.html', vault_items=vault_items)

@app.route('/upload_medical_file', methods=['POST'])
def upload_medical_file():
    if 'user_id' not in session or session.get('role') != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Determine file type
    file_type = 'image' if filename.lower().endswith(('.png', '.jpg', '.jpeg')) else 'document'
    
    # Add to vault
    vault_id = add_to_medical_vault(
        session['user_id'], 
        filename, 
        file_type, 
        file_path
    )
    
    if vault_id:
        return jsonify({'success': True, 'vault_id': vault_id})
    else:
        return jsonify({'error': 'Failed to add to vault'}), 500

@app.route('/blood_bank')
def blood_bank():
    blood_stock = get_blood_stock()
    return render_template('blood_bank.html', blood_stock=blood_stock)

@app.route('/invoices')
def invoices():
    if 'user_id' not in session or session.get('role') != 'patient':
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    patient_invoices = get_patient_invoices(session['user_id'])
    return render_template('patient/invoices.html', invoices=patient_invoices)

if __name__ == '__main__':
    print("--- MedTrack AWS Setup Complete ---")
    print("Initializing DynamoDB Tables...")
    try:
        create_tables()
    except Exception as e:
        print(f"Warning: Could not create tables (Check AWS Credentials): {e}")

    print("Starting MedTrack Server with AWS Integration...")
    print(f"Server started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    app.run(host='0.0.0.0', port=5000, debug=True)
