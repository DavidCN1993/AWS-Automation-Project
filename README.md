# AWS Automation Project

This project demonstrates automation of AWS infrastructure using Python and the AWS SDK (`boto3`). It automates the setup of an EC2 instance and an S3 bucket in AWS, with Nginx installed on the EC2 instance.

## Features
- Launches an EC2 instance with Nginx pre-installed.
- Creates an S3 bucket and applies tags for better organization.
- Uses Python for scripting and automation with the AWS SDK (`boto3`).

## Prerequisites
- Python 3.x
- AWS CLI configured
- `boto3` library installed

To install the `boto3` library, you can run:
```bash
pip install boto3
```

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/DavidCN1993/AWS-Automation-Project.git
   ```
2. Navigate to the project folder:
   ```bash
   cd AWS-Automation-Project
   ```
3. Run the Python script:
   ```bash
   python aws_automation.py
   ```

This script will:
- Launch an EC2 instance.
- Install and configure Nginx.
- Create an S3 bucket and apply tags.
- Display the EC2 instance's public IP and the created S3 bucket's name.

## Example Output
- **EC2 Instance ID**: i-xxxxxxxxxxxxxxxxx
- **EC2 Public IP**: 54.xxx.xxx.xxx
- **S3 Bucket Name**: f-devops-project-1

## License
This project is licensed under the MIT License.