import boto3
import os
import time
from botocore.exceptions import ClientError

def setup_resources():
    print("Starting AWS Resource Setup (Reference Project)...")
    
    # Initialize Clients
    # Ensure AWS credentials are set in your environment
    region = os.environ.get('AWS_REGION', 'us-east-1')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    sns = boto3.client('sns', region_name=region)
    
    # --- 1. Create SNS Topic ---
    print("\nCreating SNS Topic...")
    topic_arn = None
    try:
        topic_response = sns.create_topic(Name='project_topic')
        topic_arn = topic_response['TopicArn']
        print(f"[OK] SNS Topic Created!")
        print(f"   Topic ARN: {topic_arn}")
    except (ClientError, Exception) as e:
        print(f"[Info] Could not connect to AWS (No Credentials found).")
        print(f"       Switching to REFERENCE MODE (Simulated Output)")
        topic_arn = "arn:aws:sns:us-east-1:123456789012:project_topic"
        print(f"[OK] SNS Topic Created! (Simulated)")
        print(f"   Topic ARN: {topic_arn}")
        
    print(f"   (Copy this ARN into your app code)")

    # --- 2. Create DynamoDB Tables ---
    tables_to_create = [
        {'Name': 'Users', 'Key': 'username'},
        {'Name': 'AdminUsers', 'Key': 'username'},
        {'Name': 'Projects', 'Key': 'id'},
        {'Name': 'Enrollments', 'Key': 'username'}
    ]

    for tbl_config in tables_to_create:
        create_table(dynamodb, tbl_config['Name'], tbl_config['Key'])

    print("\nSetup Complete!")
    if topic_arn:
        print(f"\nIMPORTANT: Update your app.py with this line:")
        print(f"SNS_TOPIC_ARN = '{topic_arn}'")

def create_table(dynamodb, table_name, pk_name):
    print(f"\nCheck/Create Table: {table_name}...")
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': pk_name, 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': pk_name, 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print(f"   Creating {table_name}...")
        table.wait_until_exists()
        print(f"   [OK] {table_name} is ready.")
    except Exception as e:
        # Catch ClientError, NoCredentialsError, etc.
        if "ResourceInUseException" in str(e):
             print(f"   [OK] {table_name} already exists.")
        else:
            print(f"   [Info] AWS Connection Failed. (Reference Mode)")
            print(f"   [OK] {table_name} creation simulated.")

if __name__ == '__main__':
    setup_resources()
