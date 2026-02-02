# 🔧 AWS Configuration Guide for MedTrack

## ✅ GitHub Connected Successfully!

Your code is now live at: **https://github.com/prasannabme2022/AWS-Captone-project**

---

## 📋 What's Next: Configure AWS Services

Now that your code is on GitHub, you need to set up the AWS infrastructure to make your application work.

---

## 🗄️ Step 1: Create DynamoDB Tables

### Option A: Automatic Setup (Recommended)

Your `aws_setup.py` file is ready to create all tables automatically, but first you need to set up AWS credentials.

### Option B: Manual Creation via AWS Console

1. **Go to AWS Console:** https://console.aws.amazon.com/dynamodb/

2. **Create 8 Tables** (one by one):

#### Table 1: medtrack_patients
```
Table Name: medtrack_patients
Primary Key: email (String)
Read Capacity: 5 (On-Demand or Free Tier)
Write Capacity: 5
```

#### Table 2: medtrack_doctors
```
Table Name: medtrack_doctors
Primary Key: email (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 3: medtrack_appointments
```
Table Name: medtrack_appointments
Primary Key: appointment_id (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 4: medtrack_medical_vault
```
Table Name: medtrack_medical_vault
Primary Key: vault_id (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 5: medtrack_blood_bank
```
Table Name: medtrack_blood_bank
Primary Key: blood_group (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 6: medtrack_invoices
```
Table Name: medtrack_invoices
Primary Key: invoice_id (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 7: medtrack_chat_messages
```
Table Name: medtrack_chat_messages
Primary Key: message_id (String)
Read Capacity: 5
Write Capacity: 5
```

#### Table 8: medtrack_mood_logs
```
Table Name: medtrack_mood_logs
Primary Key: mood_id (String)
Read Capacity: 5
Write Capacity: 5
```

**💡 Tip:** Start with "On-Demand" pricing for development/testing.

---

## 📬 Step 2: Create SNS Topic for Notifications

### Via AWS Console:

1. **Go to SNS Console:** https://console.aws.amazon.com/sns/

2. **Create Topic:**
   - Type: **Standard**
   - Name: **medtrack_notifications**
   - Click "Create topic"

3. **Create Subscription:**
   - Protocol: **Email** (or SMS)
   - Endpoint: Your email address
   - Click "Create subscription"

4. **Confirm Subscription:**
   - Check your email
   - Click the confirmation link

5. **Copy Topic ARN:**
   - Should look like: `arn:aws:sns:us-east-1:123456789012:medtrack_notifications`
   - Save this for later!

---

## 🔐 Step 3: Create IAM User & Get Credentials

### Create IAM User:

1. **Go to IAM Console:** https://console.aws.amazon.com/iam/

2. **Create User:**
   - Users → Add users
   - User name: **medtrack-app-user**
   - Access type: **Programmatic access** ✅

3. **Attach Policies:**
   - ✅ `AmazonDynamoDBFullAccess`
   - ✅ `AmazonSNSFullAccess`

4. **Create User & Download Credentials:**
   - Download the CSV file
   - Contains: `Access Key ID` and `Secret Access Key`
   - **⚠️ KEEP THIS SECURE!** You won't see the secret key again.

---

## 🔑 Step 4: Configure Environment Variables

### Create .env File

In your project directory, create a file named `.env`:

```bash
# Create .env file
notepad .env
```

### Add These Lines:

```env
# Flask Configuration
SECRET_KEY=your-random-secret-key-here-change-this
FLASK_ENV=production

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...YOUR_ACCESS_KEY_HERE
AWS_SECRET_ACCESS_KEY=your/secret/access/key/here

# SNS Configuration
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:medtrack_notifications
```

### Generate SECRET_KEY:

```python
# Run this in Python to generate a secure secret key
import secrets
print(secrets.token_hex(32))
```

### Example .env File:

```env
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
FLASK_ENV=production
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:medtrack_notifications
```

**⚠️ IMPORTANT:** Never commit `.env` to Git! (Already in `.gitignore`)

---

## 🧪 Step 5: Test Locally

### Install Dependencies:

```bash
# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements-lite.txt
```

### Run the Application:

```bash
python aws_setup.py
```

### Expected Output:

```
--- MedTrack AWS Setup Complete ---
Starting MedTrack Server with AWS Integration...
Server started at 2026-02-02 09:30:00
 * Serving Flask app 'aws_setup'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

### Test in Browser:

Open: **http://localhost:5000**

You should see the MedTrack homepage!

---

## ✅ Verify Everything Works

### Test Patient Registration:

1. Go to: http://localhost:5000/signup
2. Register as a Patient
3. Fill in all details
4. Submit

**Expected:**
- ✅ Patient created in DynamoDB
- ✅ SNS notification sent to your email
- ✅ Redirect to login page

### Test Doctor Registration:

1. Register as a Doctor
2. Add specialization and license number

**Expected:**
- ✅ Doctor created in DynamoDB
- ✅ SNS notification received

### Test Appointment Booking:

1. Login as Patient
2. Book an appointment with a doctor
3. Check your email for notification

**Expected:**
- ✅ Appointment created in DynamoDB
- ✅ SNS notification sent

### Verify in AWS Console:

**DynamoDB:**
- Go to: https://console.aws.amazon.com/dynamodb/
- Click "Tables"
- Click "medtrack_patients"
- Click "Explore table items"
- You should see your patient record!

**SNS:**
- Check your email inbox
- You should have received notifications

---

## ☁️ Step 6: Deploy to AWS EC2 (Optional)

### Launch EC2 Instance:

1. **Go to EC2 Console:** https://console.aws.amazon.com/ec2/

2. **Launch Instance:**
   - Name: **medtrack-server**
   - AMI: **Amazon Linux 2023** or **Ubuntu 22.04**
   - Instance type: **t2.micro** (Free Tier)
   - Key pair: Create new or use existing
   - Security Group:
     - SSH (22) - Your IP only
     - HTTP (80) - 0.0.0.0/0
     - Custom TCP (5000) - 0.0.0.0/0

3. **Launch Instance**

### Connect to EC2:

```bash
# Download your .pem file first
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP
```

### Setup on EC2:

```bash
# Update system
sudo yum update -y  # Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Python and Git
sudo yum install python3 python3-pip git -y  # Amazon Linux
# OR
sudo apt install python3 python3-pip git -y  # Ubuntu

# Clone your repository
git clone https://github.com/prasannabme2022/AWS-Captone-project.git
cd AWS-Captone-project

# Install dependencies
pip3 install -r requirements-lite.txt

# Create .env file
nano .env
# Paste your AWS credentials and configuration

# Run the app
python3 aws_setup.py
```

### Access Your App:

```
http://YOUR_EC2_PUBLIC_IP:5000
```

---

## 📊 Monitor Your Application

### CloudWatch (Optional):

Set up CloudWatch alarms for:
- DynamoDB throttling
- EC2 CPU usage
- Application errors

### Cost Monitoring:

- Go to: https://console.aws.amazon.com/billing/
- Set up billing alerts
- Monitor Free Tier usage

---

## 🎯 Post-Deployment Checklist

- [ ] All 8 DynamoDB tables created
- [ ] SNS topic created and email confirmed
- [ ] IAM user created with proper permissions
- [ ] `.env` file configured with credentials
- [ ] Application runs locally
- [ ] Patient registration works
- [ ] Doctor registration works
- [ ] Appointment booking works
- [ ] SNS notifications received
- [ ] DynamoDB tables populated with test data
- [ ] (Optional) EC2 instance deployed
- [ ] (Optional) Domain name configured
- [ ] (Optional) HTTPS/SSL certificate added

---

## 🆘 Troubleshooting

### Error: "Unable to locate credentials"

**Solution:**
- Check `.env` file exists
- Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are correct
- Ensure python-dotenv is installed

### Error: "ResourceNotFoundException"

**Solution:**
- DynamoDB table doesn't exist
- Create tables manually or check table names match exactly

### Error: "InvalidClientTokenId"

**Solution:**
- AWS credentials are invalid
- Regenerate IAM access keys

### Error: SNS notifications not received

**Solution:**
- Check SNS subscription is confirmed
- Verify SNS_TOPIC_ARN is correct
- Check spam folder

---

## 📞 Support Resources

- **AWS Documentation:** https://docs.aws.amazon.com/
- **DynamoDB Guide:** https://docs.aws.amazon.com/dynamodb/
- **SNS Guide:** https://docs.aws.amazon.com/sns/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Boto3 Documentation:** https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

---

## 🎉 Congratulations!

Once you complete these steps, you'll have a fully functional, cloud-powered healthcare management system running on AWS!

**Your MedTrack Application:**
- ✅ Code on GitHub
- ✅ Data in DynamoDB
- ✅ Notifications via SNS
- ✅ Hosted on EC2 (optional)
- ✅ Production-ready!

---

**Last Updated:** February 2, 2026  
**Status:** Ready for AWS Configuration  
**Next Step:** Create DynamoDB tables
