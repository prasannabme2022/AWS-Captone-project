# 🔐 MedTrack Login Credentials (For Testing)

## ✅ Test Users Available

Your app now uses the in-memory database which comes with pre-configured test users!

### 👤 Patient Login
```
Email: patient@example.com
Password: password123
```
**What you can do:**
- View patient dashboard
- Book appointments with doctors
- Upload medical reports to vault
- Use AI assistant for health queries
- View and pay invoices
- Track mood
- Chat with doctors

---

### 👨‍⚕️ Doctor Login
```
Email: doctor@example.com
Password: password123
```
**What you can do:**
- View doctor dashboard
- See all appointments
- Review patient medical records
- Update appointment status
- Use AI-powered multimodal diagnostics
- Chat with patients

---

### 🔧 Admin Login
```
Email: admin@example.com
Password: password123
```
**What you can do:**
- Manage blood bank inventory
- Monitor hospital capacity
- View all patients
- Approve blood donations
- System administration

---

## 🚀 How to Use

### Step 1: Run the Application
```bash
python app.py
```

### Step 2: Open Browser
Go to: **http://127.0.0.1:5000** or **http://localhost:5000**

### Step 3: Login
Click "Login" and use any of the credentials above!

---

## 📋 What Changed?

I switched your `app.py` from using AWS DynamoDB to the in-memory database:

**Before (Line 3-4):**
```python
# import database # Old In-Memory DB
import database_dynamo as database # New AWS DynamoDB Adapter
```

**After (Line 3-4):**
```python
import database # In-Memory DB (for local testing)
# import database_dynamo as database # AWS DynamoDB Adapter (use when AWS is configured)
```

### Why?
- ✅ No AWS credentials needed
- ✅ Works immediately for testing
- ✅ All features work locally
- ✅ Pre-loaded test data (users, doctors, blood bank)

---

## 🔄 To Switch Back to AWS Later

When you configure AWS and want to use DynamoDB:

1. Stop the app (Ctrl+C)
2. Edit `app.py` line 3-4:
   ```python
   # import database # In-Memory DB (for local testing)
   import database_dynamo as database # AWS DynamoDB Adapter
   ```
3. Create `.env` file with AWS credentials
4. Restart the app

---

## 📊 Pre-Loaded Data

### Doctors Available:
1. **Dr. Rajesh Koothrappali** - Cardiology
2. **Dr. Priya Sethi** - Dermatology
3. **Dr. Sanjay Gupta** - General Medicine
4. **Dr. Anjali Menon** - Pediatrics
5. **Dr. Sameer Khan** - Orthopedics

### Blood Bank Stock:
- A+: 15 units
- B+: 22 units
- O+: 30 units
- AB+: 10 units
- A-: 4 units (Low)
- B-: 6 units
- O-: 2 units (Critical)
- AB-: 3 units (Low)

---

## 🧪 Testing Checklist

Try these features:

### As Patient:
- [ ] Login
- [ ] Book appointment with a doctor
- [ ] Upload a medical report
- [ ] Chat with AI assistant
- [ ] View invoices
- [ ] Log mood
- [ ] Chat with doctor

### As Doctor:
- [ ] Login
- [ ] View appointments
- [ ] Update appointment status
- [ ] View patient medical records
- [ ] Use multimodal AI diagnostics
- [ ] Reply to patient chats

### As Admin:
- [ ] Login
- [ ] View blood bank
- [ ] Update blood stock
- [ ] View hospital capacity
- [ ] Approve blood donations
- [ ] View all patients

---

## ⚠️ Important Notes

### This is for LOCAL TESTING ONLY!
- Data is stored in memory (lost when app restarts)
- Not suitable for production
- Use AWS DynamoDB for production (see aws_setup.py)

### For AWS Production:
Use the `aws_setup.py` file instead which has:
- DynamoDB integration
- SNS notifications
- Proper data persistence
- Scalability

---

## 🆘 Troubleshooting

### Can't login?
- Make sure you're using exact credentials (case-sensitive)
- Email: **patient@example.com** (not patient@test.com)
- Password: **password123**

### App won't start?
```bash
# Install dependencies
pip install -r requirements-lite.txt

# Try again
python app.py
```

### Port already in use?
```bash
# Change port in app.py line 572:
app.run(host="0.0.0.0", port=5001, debug=True)  # Change 5000 to 5001
```

---

## 🎯 Next Steps

1. **Test Locally** ✅ ← You can do this now!
2. **Configure AWS** (when ready)
3. **Switch to aws_setup.py** for production
4. **Deploy to EC2** (optional)

---

**Happy Testing! 🎉**

The app is now running with sample data and ready to use!
