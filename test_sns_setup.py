import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
REGION = os.getenv('AWS_REGION', 'ap-south-1')
TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:050690756868:Medtrack_cloud_enabled_healthcare_management')

print(f"--- Testing MedTrack SNS Configuration ---")
print(f"Region: {REGION}")
print(f"Topic ARN: {TOPIC_ARN}")

try:
    # 1. Initialize Client
    print("\n1. Initializing SNS Client...")
    # Parse region from ARN if possible, often safer than assuming default
    if 'arn:aws:sns:' in TOPIC_ARN:
        arn_parts = TOPIC_ARN.split(':')
        arn_region = arn_parts[3]
        print(f"   Detected Region from ARN: {arn_region}")
        client = boto3.client('sns', region_name=arn_region)
    else:
        client = boto3.client('sns', region_name=REGION)
    print("   Client initialized.")

    # 2. Check Topic Attributes (Verify existence)
    print("\n2. Verifying Topic Existence...")
    client.get_topic_attributes(TopicArn=TOPIC_ARN)
    print("   Topic exists and is accessible!")

    # 3. Send Test Notification
    print("\n3. Sending Test Verification Message...")
    response = client.publish(
        TopicArn=TOPIC_ARN,
        Message="This is a test message from MedTrack Server verification.",
        Subject="MedTrack Connectivity Check"
    )
    print(f"   Success! Message ID: {response['MessageId']}")
    print("\n✅ SNS Service is WORKING PROPERLY.")

except Exception as e:
    print(f"\n❌ ERROR: SNS Service check FAILED.")
    print(f"   Error Details: {e}")
    print("\nTroubleshooting Steps:")
    print("   1. Check if AWS Credentials are set in .env or ~/.aws/credentials")
    print("   2. Verify the SNS_TOPIC_ARN in .env matches your AWS Console")
    print("   3. Ensure the Region in .env matches the Topic's region")
