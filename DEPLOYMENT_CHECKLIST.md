# ✅ AWS MedTrack - Deployment Checklist

## 📋 Pre-Deployment Checklist

### 1. Code Files ✅
- [x] `aws_setup.py` - Updated with DynamoDB & SNS integration
- [x] `requirements.txt` - Full dependencies with boto3
- [x] `requirements-lite.txt` - Lightweight version
- [x] `README.md` - Comprehensive documentation
- [x] `GIT_DEPLOYMENT.md` - Git deployment instructions
- [x] `PUSH_TO_GITHUB.md` - Step-by-step GitHub push guide

### 2. AWS Services Configuration ⚙️

#### DynamoDB Tables (8 tables required):
- [ ] `medtrack_patients`
- [ ] `medtrack_doctors`
- [ ] `medtrack_appointments`
- [ ] `medtrack_medical_vault`
- [ ] `medtrack_blood_bank`
- [ ] `medtrack_invoices`
- [ ] `medtrack_chat_messages`
- [ ] `medtrack_mood_logs`

**To create tables:**
```bash
python aws_setup.py
```

#### SNS Topic:
- [ ] Create SNS topic: `medtrack_notifications`
- [ ] Subscribe your email/phone for notifications
- [ ] Note the Topic ARN

**AWS Console Steps:**
1. Go to AWS SNS Console
2. Create Topic → Standard
3. Name: `medtrack_notifications`
4. Create subscription → Email/SMS
5. Copy Topic ARN

#### IAM Credentials:
- [ ] AWS Access Key ID created
- [ ] AWS Secret Access Key saved securely
- [ ] IAM user has permissions for:
  - DynamoDB (read/write)
  - SNS (publish)
  - EC2 (if deploying to EC2)

---

## 🔐 Environment Variables

Create `.env` file with:

```env
# Flask Configuration
SECRET_KEY=<generate-random-secret-key>
FLASK_ENV=production

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>

# SNS Configuration
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:<account-id>:medtrack_notifications
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

---

## 🚀 GitHub Repository Checklist

### Before Pushing:
- [ ] Git installed and configured
- [ ] GitHub account accessible
- [ ] Repository URL confirmed: https://github.com/prasannabme2022/AWS-Captone-project.git
- [ ] `.gitignore` file present (excludes .env, uploads, __pycache__)
- [ ] Personal Access Token generated (if using HTTPS)

### Files to Push:
- [ ] `aws_setup.py`
- [ ] `requirements.txt`
- [ ] `requirements-lite.txt`
- [ ] `README.md`
- [ ] All template files (HTML)
- [ ] Static files (CSS, JS)
- [ ] Other Python files (ml_engine.py, database_dynamo.py, etc.)

### Files to EXCLUDE (in .gitignore):
- [ ] `.env` (contains AWS credentials!)
- [ ] `uploads/*` (medical files - privacy)
- [ ] `__pycache__/`
- [ ] `*.pyc`
- [ ] `venv/`

---

## 🧪 Testing Checklist

### Local Testing:
- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] AWS credentials configured in `.env`
- [ ] DynamoDB tables created
- [ ] App runs locally: `python aws_setup.py`
- [ ] Access app at: http://localhost:5000
- [ ] Test patient signup
- [ ] Test doctor signup
- [ ] Test appointment booking
- [ ] Test AI chatbot
- [ ] Test file upload to medical vault

### AWS Services Testing:
- [ ] DynamoDB: Can create/read patient records
- [ ] DynamoDB: Can create/read appointments
- [ ] SNS: Receiving notifications on registration
- [ ] SNS: Receiving notifications on appointment booking

---

## ☁️ EC2 Deployment Checklist (Optional)

### EC2 Instance:
- [ ] Instance launched (t2.micro for free tier)
- [ ] Security Group configured:
  - Port 22 (SSH) - Your IP only
  - Port 80 (HTTP) - 0.0.0.0/0
  - Port 443 (HTTPS) - 0.0.0.0/0
  - Port 5000 (Flask) - 0.0.0.0/0 (or use nginx)
- [ ] Key pair (.pem file) downloaded and secure
- [ ] Elastic IP assigned (optional, for static IP)

### Server Setup:
- [ ] SSH access working
- [ ] Python 3.9+ installed
- [ ] pip installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] `.env` file created with AWS credentials
- [ ] DynamoDB tables accessible from EC2
- [ ] App running on server
- [ ] Access app via public IP

---

## 📊 Feature Verification

### Patient Features:
- [ ] Patient registration working
- [ ] Patient login working
- [ ] Patient dashboard displays
- [ ] Book appointment feature
- [ ] AI chatbot responds
- [ ] Medical vault file upload
- [ ] View appointments
- [ ] View invoices
- [ ] Mood tracking logs

### Doctor Features:
- [ ] Doctor registration working
- [ ] Doctor login working
- [ ] Doctor dashboard displays
- [ ] View patient appointments
- [ ] Add diagnosis
- [ ] Add prescription
- [ ] Update appointment status
- [ ] Chat with patients

### Admin Features:
- [ ] Blood bank display
- [ ] Update blood stock
- [ ] View all users
- [ ] System notifications

---

## 🔒 Security Checklist

- [ ] `.env` file NOT in Git repository
- [ ] SECRET_KEY is random and strong
- [ ] AWS credentials not hardcoded
- [ ] Password hashing enabled (Werkzeug)
- [ ] Session security configured
- [ ] DynamoDB encryption at rest enabled
- [ ] IAM user has minimal required permissions
- [ ] HTTPS enabled (for production)
- [ ] File upload validation in place
- [ ] SQL injection protected (using DynamoDB, low risk)

---

## 📈 Performance Checklist

- [ ] DynamoDB capacity appropriate (start with 5 RCU/WCU)
- [ ] Images/files compressed before upload
- [ ] Static files served efficiently
- [ ] Database queries optimized
- [ ] Error handling in place
- [ ] Logging configured

---

## 📝 Documentation Checklist

- [x] README.md with setup instructions
- [x] Deployment guide
- [x] Architecture diagram (if needed)
- [ ] API documentation (if applicable)
- [ ] User manual (optional)
- [x] Troubleshooting guide

---

## 🎯 Post-Deployment Tasks

### After Successful Deployment:
- [ ] Test all features on production
- [ ] Subscribe to SNS notifications
- [ ] Monitor DynamoDB usage
- [ ] Monitor EC2 instance (if used)
- [ ] Set up CloudWatch alarms (optional)
- [ ] Configure backup strategy
- [ ] Document any production issues
- [ ] Share repository with team/reviewers

---

## 🆘 Emergency Contacts

- AWS Support: https://console.aws.amazon.com/support/home
- GitHub Support: https://support.github.com
- Stack Overflow: https://stackoverflow.com/questions/tagged/flask+aws

---

## 📊 Cost Monitoring

### Free Tier Limits:
- **DynamoDB:** 25 GB storage, 25 RCU/WCU
- **SNS:** 1,000 email notifications/month
- **EC2:** 750 hours/month (t2.micro)

**Monitor usage at:**
https://console.aws.amazon.com/billing/home

---

## ✅ Final Checks Before Going Live

- [ ] All features tested
- [ ] Error pages customized
- [ ] Contact information updated
- [ ] Privacy policy added (if collecting health data)
- [ ] Terms of service added
- [ ] Backup strategy in place
- [ ] Monitoring alerts configured
- [ ] Team trained on system

---

## 🎉 Ready to Deploy!

If all checkboxes are marked, you're ready to:
1. Push code to GitHub
2. Deploy to AWS EC2 (optional)
3. Share with users/reviewers
4. Monitor and maintain

---

**Last Updated:** 2026-02-02
**Project:** MedTrack - Cloud-Enabled Healthcare Management System
**Repository:** https://github.com/prasannabme2022/AWS-Captone-project
