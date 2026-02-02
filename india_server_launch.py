import boto3
import os
import time

def launch_india_server():
    """
    Launches an EC2 instance in the India (ap-south-1) region.
    """
    print("🚀 Initiating Launch Sequence for India Server (ap-south-1)...")
    
    # Configuration
    REGION = 'ap-south-1'
    AMI_ID = 'ami-0f5ee92e2d63afc18' # Amazon Linux 2023 AMI in ap-south-1 (Verify before use)
    INSTANCE_TYPE = 't2.micro'
    KEY_NAME = 'medtrack-india-key'
    SECURITY_GROUP_NAME = 'medtrack-sg-india'
    
    try:
        # Initialize EC2 client
        ec2 = boto3.client('ec2', region_name=REGION)
        ec2_resource = boto3.resource('ec2', region_name=REGION)
        
        print(f"✅ Connected to AWS Region: {REGION}")
        
        # 1. Create Key Pair (if not exists)
        try:
            print("🔑 Checking Key Pair...")
            key_pair = ec2.create_key_pair(KeyName=KEY_NAME)
            print(f"   Created new key pair: {KEY_NAME}")
            # Save private key locally
            with open(f"{KEY_NAME}.pem", "w") as private_key_file:
                private_key_file.write(key_pair['KeyMaterial'])
            print(f"   Saved private key to {KEY_NAME}.pem")
        except Exception as e:
            if 'InvalidKeyPair.Duplicate' in str(e):
                print(f"   Key pair {KEY_NAME} already exists. Using existing one.")
            else:
                print(f"   Error creating key pair: {e}")

        # 2. Create Security Group
        try:
            print("🛡️ Checking Security Group...")
            response = ec2.describe_security_groups(
                Filters=[dict(Name='group-name', Values=[SECURITY_GROUP_NAME])]
            )
            
            if response['SecurityGroups']:
                sg_id = response['SecurityGroups'][0]['GroupId']
                print(f"   Security Group {SECURITY_GROUP_NAME} already exists ({sg_id}).")
            else:
                sg = ec2.create_security_group(
                    GroupName=SECURITY_GROUP_NAME,
                    Description='Allow HTTP and SSH for MedTrack India Server'
                )
                sg_id = sg['GroupId']
                
                # Add Rules
                ec2.authorize_security_group_ingress(
                    GroupId=sg_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 80,
                            'ToPort': 80,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        },
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 5000,
                            'ToPort': 5000,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        },
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )
                print(f"   Created Security Group: {sg_id}")
        except Exception as e:
            print(f"   Error setting up Security Group: {e}")
            return

        # 3. Launch Instance
        print(f"🖥️ Launching EC2 Instance ({INSTANCE_TYPE})...")
        instances = ec2_resource.create_instances(
            ImageId=AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SecurityGroupIds=[sg_id],
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'MedTrack-India-Server'}]
            }],
            # User Data to install dependencies and run app
            UserData='''#!/bin/bash
            yum update -y
            yum install -y python3 git
            pip3 install flask boto3 waitress
            echo "MedTrack Server Initialized" > /home/ec2-user/status.txt
            '''
        )
        
        instance = instances[0]
        print(f"   Instance Created! ID: {instance.id}")
        print("   Waiting for instance to run...")
        instance.wait_until_running()
        instance.reload()
        
        print(f"\n✅ Server Deployed Successfully in India!")
        print(f"   Public IP: {instance.public_ip_address}")
        print(f"   Public DNS: {instance.public_dns_name}")
        print(f"   Region: {REGION}")
        
    except Exception as e:
        print(f"\n❌ Setup Failed: {e}")
        print("Note: Ensure you have valid AWS credentials configured for ap-south-1.")

if __name__ == "__main__":
    launch_india_server()
