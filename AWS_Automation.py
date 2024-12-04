import boto3 # type: ignore
import json

# Initialize AWS clients for EC2 and S3
region = 'eu-north-1'
ec2 = boto3.client('ec2', region_name=region)
s3 = boto3.client('s3', region_name=region)

# Define the user_data script to install and configure Nginx
user_data_script = """#!/bin/bash
sudo apt update
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
echo "<h1>Welcome to Nginx on AWS</h1>" | sudo tee /var/www/html/index.html
"""

def launch_ec2_instance():
    try:
        # Launch EC2 instance
        response = ec2.run_instances(
            ImageId='ami-08eb150f611ca277f',  # Ubuntu AMI ID for 'eu-north-1'
            InstanceType='t3.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='Linux-Key',  # Replace with your key pair name
            SecurityGroupIds=['sg-089b89da56b386651'],  # Replace with your Security Group ID
            SubnetId='subnet-04debdcf8c14ed74a',  # Replace with your Subnet ID
            UserData=user_data_script
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 Instance Launched: {instance_id}")
        
        # Wait for the instance to initialize and retrieve its public IP
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        instance_details = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance_details['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(f"Instance Public IP: {public_ip}")
        
        # Tags for the EC2 instance
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': 'DevOpsProject-EC2'},
                {'Key': 'Project', 'Value': 'DevOps-Automation'}
            ]
        )
        print("Tags added to EC2 instance.")
        return instance_id, public_ip

    except Exception as e:
        print(f"Error launching EC2 instance: {e}")
        return None, None

def create_s3_bucket(bucket_name):
    try:
        # Create S3 bucket
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        print(f"S3 Bucket Created: {bucket_name}")
        
        # Tags for the S3 bucket
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {'Key': 'Name', 'Value': 'DevOpsProject-S3'},
                    {'Key': 'Project', 'Value': 'DevOps-Automation'}
                ]
            }
        )
        print("Tags added to S3 bucket.")
        return bucket_name

    except Exception as e:
        print(f"Error creating S3 bucket: {e}")
        return None

def main():
    bucket_name = 'f-devops-project-1'  
    print("Starting AWS resource setup...")

    # Step 1: Launch EC2 instance
    instance_id, public_ip = launch_ec2_instance()
    if instance_id and public_ip:
        print(f"EC2 Instance setup complete: ID={instance_id}, Public IP={public_ip}")
    else:
        print("EC2 setup failed. Exiting.")
        return

    # Step 2: Create S3 bucket
    bucket_name = create_s3_bucket(bucket_name)
    if bucket_name:
        print(f"S3 Bucket setup complete: Name={bucket_name}")
    else:
        print("S3 setup failed. Exiting.")
        return

    print("AWS resource setup completed successfully!")

if __name__ == "__main__":
    main()
