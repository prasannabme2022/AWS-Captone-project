#!/usr/bin/env python3
"""
MedTrack DynamoDB Table Setup Script
Creates 4 tables for the hybrid schema design
"""

import boto3
import os
from botocore.exceptions import ClientError

def create_table(dynamodb, table_name, key_schema, attribute_definitions, billing_mode='PAY_PER_REQUEST'):
    """Helper function to create a DynamoDB table"""
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode=billing_mode
        )
        print(f"⏳ Creating table {table_name}...")
        table.wait_until_exists()
        print(f"✅ Table {table_name} created successfully!")
        print(f"   Table ARN: {table.table_arn}")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"✅ Table {table_name} already exists")
            return dynamodb.Table(table_name)
        else:
            print(f"❌ Error creating {table_name}: {e}")
            raise

def setup_medtrack_tables():
    """Create all 4 DynamoDB tables for MedTrack"""
    
    # Get region from environment or use default
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    
    print("=" * 70)
    print("MedTrack DynamoDB Setup")
    print(f"Region: {region}")
    print("=" * 70)
    
    try:
        dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # 1. AdminUser Table
        print("\n1️⃣  Creating AdminUser Table...")
        create_table(
            dynamodb,
            table_name='AdminUser',
            key_schema=[
                {'AttributeName': 'username', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'username', 'AttributeType': 'S'}
            ]
        )
        
        # 2. DoctorUser Table
        print("\n2️⃣  Creating DoctorUser Table...")
        create_table(
            dynamodb,
            table_name='DoctorUser',
            key_schema=[
                {'AttributeName': 'username', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'username', 'AttributeType': 'S'}
            ]
        )
        
        # 3. PatientUser Table
        print("\n3️⃣  Creating PatientUser Table...")
        create_table(
            dynamodb,
            table_name='PatientUser',
            key_schema=[
                {'AttributeName': 'username', 'KeyType': 'HASH'}
            ],
            attribute_definitions=[
                {'AttributeName': 'username', 'AttributeType': 'S'}
            ]
        )
        
        # 4. Medtrack_data Table (Single-Table Design for all other data)
        print("\n4️⃣  Creating Medtrack_data Table (Hybrid Single-Table Design)...")
        create_table(
            dynamodb,
            table_name='Medtrack_data',
            key_schema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            attribute_definitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ]
        )
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS! All 4 DynamoDB tables are ready")
        print("=" * 70)
        print("\nTable Summary:")
        print("  • AdminUser       - Admin authentication")
        print("  • DoctorUser      - Doctor authentication")
        print("  • PatientUser     - Patient authentication")
        print("  • Medtrack_data   - Appointments, Records, Invoices (PK/SK design)")
        print("\nNext Steps:")
        print("  1. Run 'python3 seed_demo_users.py' to create demo accounts")
        print("  2. Run 'python3 app.py' to start the application")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure AWS credentials are configured:")
        print("      export AWS_ACCESS_KEY_ID=your_key")
        print("      export AWS_SECRET_ACCESS_KEY=your_secret")
        print("   2. Verify you have DynamoDB permissions")
        print("   3. Set AWS_REGION if not using ap-south-1:")
        print("      export AWS_REGION=ap-southeast-2")
        return False

if __name__ == '__main__':
    success = setup_medtrack_tables()
    exit(0 if success else 1)
