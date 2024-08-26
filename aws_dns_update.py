import boto3
import requests
import os

# Update the following variables with your own information
DOMAIN = "yourdomain.com"  # Replace with your actual domain
HOSTED_ZONE_ID = "YOUR_HOSTED_ZONE_ID"  # Replace with your Route 53 hosted zone ID
RECORD_NAME = "home." + DOMAIN
TTL = 300

# AWS Credentials - Use environment variables or a credentials file for better security practices
# AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'  # Replace with your AWS access key ID
# AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'  # Replace with your AWS secret access key

# It's highly recommended to use environment variables for credentials or configure boto3 to use AWS credentials from a profile
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# File to store the last known IP address
IP_CACHE_FILE = 'last_ip.txt'

# List of domains to update - Add your domains here
domains = [
    "yourdomain.com",  # Replace with your actual domain
    "www.yourdomain.com",  # Replace with your actual domain
    "home.yourdomain.com"  # Replace with your actual domain
]

# Function to get the current public IP address
def get_current_ip():
    return requests.get('http://checkip.amazonaws.com').text.strip()

# Function to read the last known IP address from file
def read_last_ip():
    if os.path.isfile(IP_CACHE_FILE):
        with open(IP_CACHE_FILE, 'r') as file:
            return file.read().strip()
    return None

# Function to write the current IP address to file
def write_current_ip(ip):
    with open(IP_CACHE_FILE, 'w') as file:
        file.write(ip)

# Get the current public IP address
current_ip = get_current_ip()

# Get the last known IP address
last_ip = read_last_ip()

# Check if the IP address has changed
if current_ip != last_ip:
    # Create boto3 client with credentials
    client = boto3.client('route53',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    for record_name in domains:
        # Create the change batch
        change_batch = {
            'Comment': 'Updating A record for ' + record_name,
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'A',
                        'TTL': TTL,
                        'ResourceRecords': [{'Value': current_ip}]
                    }
                }
            ]
        }

        # Update the record
        response = client.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch=change_batch
        )

        print(f"Update response for {record_name}: {response}")

    # Update the IP cache file with the new IP address
    write_current_ip(current_ip)
else:
    print("IP address has not changed. No update needed.")
