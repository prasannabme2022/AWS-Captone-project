#!/usr/bin/env python3
"""
Seed demo users into DynamoDB tables
Creates demo admin, doctor, and patient accounts
"""

import boto3
import os
from werkzeug.security import generate_password_hash
from botocore.exceptions import ClientError

def seed_users():
    """Create demo users in DynamoDB"""
    
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    
    print("=" * 70)
    print("MedTrack Demo User Seeding")
    print(f"Region: {region}")
    print("=" * 70)
    
    try:
        dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Get table references
        admin_table = dynamodb.Table('AdminUser')
        doctor_table = dynamodb.Table('DoctorUser')
        patient_table = dynamodb.Table('PatientUser')
        
        # 1. Create Admin User
        print("\n1️⃣  Creating Admin User...")
        try:
            admin_table.put_item(
                Item={
                    'username': 'admin@medtrack.com',
                    'password': generate_password_hash('admin123'),
                    'name': 'System Administrator',
                    'role': 'admin',
                    'created_at': '2026-02-04T00:00:00'
                },
                ConditionExpression='attribute_not_exists(username)'
            )
            print("   ✅ Admin created: admin@medtrack.com / admin123")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print("   ⚠️  Admin already exists")
            else:
                raise
        
        # 2. Create Doctor User
        print("\n2️⃣  Creating Doctor User...")
        try:
            doctor_table.put_item(
                Item={
                    'username': 'doctor@medtrack.com',
                    'password': generate_password_hash('doctor123'),
                    'name': 'Dr. Sarah Johnson',
                    'specialization': 'General Medicine',
                    'role': 'doctor',
                    'created_at': '2026-02-04T00:00:00'
                },
                ConditionExpression='attribute_not_exists(username)'
            )
            print("   ✅ Doctor created: doctor@medtrack.com / doctor123")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print("   ⚠️  Doctor already exists")
            else:
                raise
        
        # 3. Create Patient User
        print("\n3️⃣  Creating Patient User...")
        try:
            patient_table.put_item(
                Item={
                    'username': 'patient@medtrack.com',
                    'password': generate_password_hash('patient123'),
                    'name': 'John Doe',
                    'age': '35',
                    'gender': 'Male',
                    'role': 'patient',
                    'created_at': '2026-02-04T00:00:00'
                },
                ConditionExpression='attribute_not_exists(username)'
            )
            print("   ✅ Patient created: patient@medtrack.com / patient123")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print("   ⚠️  Patient already exists")
            else:
                raise
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Demo users are ready")
        print("=" * 70)
        print("\nDemo Credentials:")
        print("  📧 Admin:   admin@medtrack.com   / admin123")
        print("  🩺 Doctor:  doctor@medtrack.com  / doctor123")
        print("  👤 Patient: patient@medtrack.com / patient123")
        print("\nYou can now login at: http://your-server-ip:5000/login")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        print("\n💡 Make sure:")
        print("   1. Tables exist (run create_dynamodb_tables.py first)")
        print("   2. AWS credentials are configured")
        return False

if __name__ == '__main__':
    success = seed_users()
    exit(0 if success else 1)
