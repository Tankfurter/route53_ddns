# AWS Route 53 Dynamic DNS Updater

This script automatically updates AWS Route 53 DNS records with your current public IP address. It's designed for use cases where your IP address changes frequently, such as when using a home internet connection with a dynamic IP.

## Features

- Automatically retrieves your current public IP address.
- Updates AWS Route 53 A records for specified domains.
- Caches the last known IP address to minimize unnecessary API calls.
- Simple configuration using environment variables for security.

## Requirements

- Python 3.6 or higher
- AWS account with Route 53 hosted zone
- AWS credentials with appropriate permissions (Route 53 access)

## Installation

1. Clone this repository
2. Schedule the script to run periodically using a cron job or other scheduling tool
