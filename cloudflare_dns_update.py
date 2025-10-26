import requests
import os

# Update the following variables with your own information
ZONE_ID = "YOUR_ZONE_ID"  # Replace with your Cloudflare Zone ID
# File to store the last known IP address
IP_CACHE_FILE = 'last_ip_cloudflare.txt'

# Cloudflare credentials - Use environment variables for better security practices
# It's highly recommended to use environment variables for credentials
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')

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

# Function to get DNS record ID from Cloudflare
def get_dns_record_id(zone_id, record_name, api_token):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'name': record_name,
        'type': 'A'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if data['success'] and len(data['result']) > 0:
        return data['result'][0]['id']
    return None

# Function to update DNS record in Cloudflare
def update_dns_record(zone_id, record_id, record_name, ip_address, api_token, ttl=300, proxied=False):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': record_name,
        'content': ip_address,
        'ttl': ttl,
        'proxied': proxied
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Function to create DNS record in Cloudflare if it doesn't exist
def create_dns_record(zone_id, record_name, ip_address, api_token, ttl=300, proxied=False):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': record_name,
        'content': ip_address,
        'ttl': ttl,
        'proxied': proxied
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Get the current public IP address
current_ip = get_current_ip()

# Get the last known IP address
last_ip = read_last_ip()

# Check if the IP address has changed
if current_ip != last_ip:
    print(f"IP address has changed from {last_ip} to {current_ip}. Updating DNS records...")

    for record_name in domains:
        try:
            # Get the DNS record ID
            record_id = get_dns_record_id(ZONE_ID, record_name, CLOUDFLARE_API_TOKEN)

            if record_id:
                # Update existing record
                response = update_dns_record(ZONE_ID, record_id, record_name, current_ip, CLOUDFLARE_API_TOKEN)
                print(f"Updated DNS record for {record_name}: {response}")
            else:
                # Create new record if it doesn't exist
                response = create_dns_record(ZONE_ID, record_name, current_ip, CLOUDFLARE_API_TOKEN)
                print(f"Created DNS record for {record_name}: {response}")

        except Exception as e:
            print(f"Error updating {record_name}: {str(e)}")

    # Update the IP cache file with the new IP address
    write_current_ip(current_ip)
    print("DNS update completed.")
else:
    print("IP address has not changed. No update needed.")
